"""Update the working tree from a configured upstream Git repository.

Configuration is loaded from config.py first, then environment variables.
The upstream reset is intentionally destructive to local tracked changes, so
this script logs that action before performing it.
"""

from importlib import import_module
from logging import (
    ERROR,
    INFO,
    FileHandler,
    StreamHandler,
    basicConfig,
    error as log_error,
    info as log_info,
    warning as log_warning,
    getLogger,
)
from os import environ, getenv, path, remove
from subprocess import CalledProcessError, run
from typing import Any, Dict, Optional

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Keep MongoDB's verbose internal logs out of the main application log.
getLogger("pymongo").setLevel(ERROR)

if path.exists("log.txt"):
    with open("log.txt", "w", encoding="utf-8"):
        pass

if path.exists("rlog.txt"):
    remove("rlog.txt")

basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        FileHandler("log.txt", encoding="utf-8"),
        StreamHandler(),
    ],
    level=INFO,
)
LOGGER = getLogger("INDRA-MLTB-UPDATE")


def load_config() -> Dict[str, Any]:
    """Load settings from config.py, falling back to environment variables."""
    try:
        settings = import_module("config")
    except ModuleNotFoundError as exc:
        # Only fall back when config.py itself is missing. If config.py imports
        # a missing dependency, surface that real configuration problem.
        if exc.name != "config":
            raise
        LOGGER.info("config.py not found; reading settings from environment.")
        settings = None

    if settings is not None:
        return {
            key: value.strip() if isinstance(value, str) else value
            for key, value in vars(settings).items()
            if not key.startswith("__")
        }

    return {
        "BOT_TOKEN": getenv("BOT_TOKEN", "").strip(),
        "DATABASE_URL": getenv("DATABASE_URL", "").strip(),
        "DATABASE_NAME": getenv("DATABASE_NAME", "mltb").strip(),
        "UPSTREAM_REPO": getenv("UPSTREAM_REPO", "").strip(),
        "UPSTREAM_BRANCH": getenv("UPSTREAM_BRANCH", "master").strip(),
    }


def load_upstream_from_database(config: Dict[str, Any], bot_id: str) -> None:
    """Load saved upstream settings from MongoDB when deployment config allows."""
    database_url = str(config.get("DATABASE_URL", "") or "").strip()
    if not database_url:
        return

    client: Optional[MongoClient] = None
    try:
        client = MongoClient(
            database_url,
            server_api=ServerApi("1"),
            serverSelectionTimeoutMS=10000,
        )
        database = client[str(config.get("DATABASE_NAME", "mltb") or "mltb")]
        old_config = database.settings.deployConfig.find_one(
            {"_id": bot_id}, {"_id": 0}
        )
        saved_config = database.settings.config.find_one({"_id": bot_id})

        config_is_eligible = old_config is None or old_config == config
        if config_is_eligible and saved_config:
            repo = saved_config.get("UPSTREAM_REPO")
            branch = saved_config.get("UPSTREAM_BRANCH")
            if isinstance(repo, str) and repo.strip():
                config["UPSTREAM_REPO"] = repo.strip()
            if isinstance(branch, str) and branch.strip():
                config["UPSTREAM_BRANCH"] = branch.strip()
    except Exception:
        LOGGER.exception("Could not load upstream settings from MongoDB.")
    finally:
        if client is not None:
            client.close()


def git(*args: str, check: bool = True):
    """Run a Git command safely without invoking a shell."""
    return run(
        ["git", *args],
        check=check,
        text=True,
        capture_output=True,
    )


def update_from_upstream(repository: str, branch: str) -> bool:
    """Fetch and reset to the selected upstream branch."""
    repository = repository.strip()
    branch = branch.strip()

    if not repository:
        LOGGER.info("No UPSTREAM_REPO configured; skipping upstream update.")
        return True
    if not branch or branch.startswith("-"):
        LOGGER.error("UPSTREAM_BRANCH is invalid.")
        return False

    try:
        # Initialize Git metadata only when this directory is not a repository.
        inside_repo = git("rev-parse", "--is-inside-work-tree", check=False)
        if inside_repo.returncode != 0:
            git("init", "-q")

        # Use a repository-local identity; do not modify global Git settings.
        git("config", "user.name", "INDRA MLTB Custom")
        git("config", "user.email", "indra-mltb@users.noreply.github.com")

        # Preserve a snapshot of current tracked/untracked files before syncing.
        git("add", "-A")
        staged_changes = git("diff", "--cached", "--quiet", check=False)
        if staged_changes.returncode == 1:
            git("commit", "-m", "Save local changes before upstream sync")
        elif staged_changes.returncode not in (0, 1):
            raise CalledProcessError(staged_changes.returncode, staged_changes.args)

        # Update or create origin without deleting the existing .git directory.
        origin_exists = git("remote", "get-url", "origin", check=False)
        if origin_exists.returncode == 0:
            git("remote", "set-url", "origin", repository)
        else:
            git("remote", "add", "origin", repository)

        LOGGER.info("Fetching configured upstream branch: %s", branch)
        git("fetch", "--prune", "origin", branch)

        # This mirrors the original updater's behavior: upstream becomes the
        # working tree. Any local tracked edits are replaced by this reset.
        LOGGER.warning(
            "Applying upstream snapshot. Local tracked changes may be replaced."
        )
        git("reset", "--hard", "FETCH_HEAD")
        LOGGER.info("Successfully updated from the configured upstream repository.")
        return True

    except CalledProcessError as exc:
        details = (exc.stderr or exc.stdout or "").strip()
        LOGGER.error("Git update failed (exit %s): %s", exc.returncode, details)
    except FileNotFoundError:
        LOGGER.error("Git is not installed or is not available in PATH.")
    except Exception:
        LOGGER.exception("Unexpected error while updating from upstream.")

    return False


def main() -> None:
    config = load_config()
    bot_token = str(config.get("BOT_TOKEN", "") or "").strip()
    if not bot_token or ":" not in bot_token:
        LOGGER.error("BOT_TOKEN is missing or invalid. Exiting.")
        raise SystemExit(1)

    bot_id = bot_token.split(":", 1)[0]
    load_upstream_from_database(config, bot_id)

    repository = str(config.get("UPSTREAM_REPO", "") or "").strip()
    branch = str(config.get("UPSTREAM_BRANCH", "master") or "master").strip()
    if not update_from_upstream(repository, branch):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
