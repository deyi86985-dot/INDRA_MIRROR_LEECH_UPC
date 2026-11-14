from time import time

from ..helper.ext_utils.bot_utils import new_task
from ..helper.telegram_helper.button_build import ButtonMaker
from ..helper.telegram_helper.message_utils import send_message, edit_message, send_file, send_photo
from ..core.config_manager import Config
from ..helper.telegram_helper.filters import CustomFilters
from ..helper.telegram_helper.bot_commands import BotCommands


@new_task
async def start(_, message):
    buttons = ButtonMaker()
    buttons.url_button(
        "📦 Source Repository", "https://github.com/anasty17/mirror-leech-telegram-bot"
    )
    buttons.url_button("🛠️ Project Home", "https://github.com/deyi86985-dot/INDRA_MIRROR_LEECH_UPC")
    buttons.url_button("📚 Commands & Help", "https://github.com/anasty17/mirror-leech-telegram-bot#readme")
    reply_markup = buttons.build_menu(2)

    if await CustomFilters.authorized(_, message):
        start_string = (
            "<b>╔══════════════════════╗</b>\n"
            "<b>   ✦ INDRA MIRROR LEECH UPC ✦</b>\n"
            "<b>╚══════════════════════╝</b>\n\n"
            "<b>⚡ Your all-in-one transfer assistant</b>\n"
            "Download • Mirror • Leech • Clone • Extract\n\n"
            "<b>🚀 What can I do?</b>\n"
            "├ Direct links, torrents, Telegram files & NZB\n"
            "├ Google Drive and Rclone transfers\n"
            "├ Telegram upload with task controls\n"
            "└ Live progress, queues and user settings\n\n"
            f"<b>📖 Getting started:</b> Send /{BotCommands.HelpCommand} to browse commands.\n"
            "<i>Built with the upstream MLTB project; customized project branding.</i>"
        )
    else:
        start_string = (
            "<b>✦ INDRA MIRROR LEECH UPC ✦</b>\n\n"
            "A powerful download, mirror and leech assistant.\n\n"
            "<b>🔒 Access restricted</b>\n"
            "You are not an authorized user. Deploy your own instance and configure "
            "AUTHORIZED_CHATS / SUDO_USERS to control access."
        )

    image = Config.START_IMAGE
    if image:
        await send_photo(message, image, start_string, reply_markup)
    else:
        await send_message(message, start_string, reply_markup)


@new_task
async def ping(_, message):
    start_time = int(round(time() * 1000))
    reply = await send_message(message, "Starting Ping")
    end_time = int(round(time() * 1000))
    await edit_message(reply, f"{end_time - start_time} ms")


@new_task
async def log(_, message):
    await send_file(message, "log.txt")
