# INDRA MIRROR LEECH UPC — Configuration Guide

This guide describes the configuration fields in `config_sample.py`. The upstream MLTB README remains the detailed reference for advanced options.

## Required Telegram credentials

| Variable | Type | Purpose | Where to get it |
|---|---|---|---|
| `BOT_TOKEN` | text | Token used by the Telegram bot account. | [@BotFather](https://t.me/BotFather) |
| `OWNER_ID` | integer | Numeric Telegram user ID of the owner. | A Telegram ID bot such as [@userinfobot](https://t.me/userinfobot) |
| `TELEGRAM_API` | integer | Telegram API application ID. | [my.telegram.org](https://my.telegram.org) |
| `TELEGRAM_HASH` | text | Telegram API application hash. | [my.telegram.org](https://my.telegram.org) |

## Optional appearance settings

| Variable | Purpose |
|---|---|
| `START_IMAGE` | Optional image shown with `/start`. Accepts a Telegram photo `file_id` or a direct image URL. Empty means text-only. |
| `HELP_IMAGE` | Optional image shown with `/help`. Accepts a Telegram photo `file_id` or a direct image URL. Empty means text-only. |

## Access and database

| Variable | Purpose |
|---|---|
| `AUTHORIZED_CHATS` | Chats/users allowed to run commands. |
| `SUDO_USERS` | Additional trusted administrators. |
| `DATABASE_URL` | MongoDB connection URI. Treat as a password. |
| `DATABASE_NAME` | Database name; default is `mltb`. |
| `TG_PROXY` | Optional Telegram proxy settings dictionary. |
| `USER_SESSION_STRING` | Optional user account session for supported user-session features. Highly sensitive; never share it. |

## Transfer and status settings

| Variable | Purpose |
|---|---|
| `DEFAULT_UPLOAD` | Default upload destination (`rc`, `gd`, `bh`, or `gf`, subject to configured services). |
| `STATUS_LIMIT` | Number of tasks shown per status page. |
| `STATUS_UPDATE_INTERVAL` | Automatic status refresh interval in seconds. |
| `LEECH_SPLIT_SIZE` | Split threshold for Telegram leech uploads; `0` uses the project default behaviour. |
| `AS_DOCUMENT` | Upload leech files as documents when enabled. |
| `EQUAL_SPLITS` | Use equal-sized split parts when enabled. |
| `MEDIA_GROUP` | Send split parts in media groups when enabled. |
| `USER_TRANSMISSION` | Enable supported user-session transmission behaviour. |
| `HYBRID_LEECH` | Enable supported hybrid bot/user upload behaviour. |
| `LEECH_DUMP_CHAT` | Optional destination for leech dump messages. |
| `THUMBNAIL_LAYOUT` | Optional custom thumbnail layout configuration. |
| `FILES_LINKS` | Enable supported file-link buttons in leech output. |

## Cloud and external service settings

The remaining fields in `config_sample.py` configure optional services. Leave them empty/disabled if you do not use that service.

- **Google Drive:** `GDRIVE_ID`, `IS_TEAM_DRIVE`, `STOP_DUPLICATE`, `INDEX_URL`, service-account options.
- **Rclone:** `RCLONE_PATH`, `RCLONE_FLAGS`, `RCLONE_SERVE_*`, `UPLOAD_PATHS`.
- **JDownloader:** `JD_EMAIL`, `JD_PASS`.
- **SABnzbd / NZB:** `USENET_SERVERS`, `HYDRA_IP`, `HYDRA_API_KEY`.
- **Download services:** `ALLDEBRID_API_KEY`, `BUZZHEAVIER_*`, `GOFILE_API_KEY`, `FILELION_API`, `STREAMWISH_API`, `TLDV_TOKEN`.
- **Yt-dlp / Gallery-dl / FFmpeg:** `YT_DLP_OPTIONS`, `GALLERY_DL_OPTIONS`, `FFMPEG_CMDS`, `NAME_SUBSTITUTE`.
- **Queue and RSS:** `QUEUE_*`, `RSS_*`.
- **Torrent / web interface:** `TORRENT_TIMEOUT`, `BASE_URL`, `BASE_URL_PORT`, `WEB_PINCODE`, `SEARCH_*`.
- **Update source:** `UPSTREAM_REPO`, `UPSTREAM_BRANCH`.

## Important security checklist

- Never commit `config.py`, `.env`, Telegram session strings, bot tokens, API hashes, database URIs, cookies or service-account JSON files.
- Keep the repository private if you are unsure what files contain secrets.
- Rotate any credential that was accidentally posted publicly.
- Use only image URLs/file IDs for images you own or are authorized to use.
- Do not change advanced settings unless you understand their effect; invalid values can prevent startup or transfers.

## Telegram button colours

This build assigns supported semantic button styles: **green** for positive/confirm actions, **red** for cancel/close/delete actions and **blue** for navigation/help actions. Actual rendering depends on Telegram Bot API support and the user's Telegram client; Telegram does not provide arbitrary custom hex colours for inline buttons.

## Upstream documentation

- [Original MLTB repository](https://github.com/anasty17/mirror-leech-telegram-bot)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram API credentials](https://my.telegram.org)
