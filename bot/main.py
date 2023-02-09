import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.error import Forbidden, NetworkError
import asyncio
import logging
from typing import NoReturn
from telegram import __version__ as ptb_version

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"Этот бот несовместим с вашей текущей версией PTB {ptb_version}."
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main() -> NoReturn:
    """Запуск бота."""
    async with Bot(TELEGRAM_TOKEN) as bot:
        try:
            update_id = (await bot.get_updates())[0].update_id
        except IndexError:
            update_id = None

        logger.info("listening for new messages...")
        while True:
            try:
                update_id = await hello(bot, update_id)
            except NetworkError:
                await asyncio.sleep(1)
            except Forbidden:
                update_id += 1


async def hello(bot: Bot, update_id: int) -> int:
    """На любое сообщение отвечает одной фразой."""
    updates = await bot.get_updates(offset=update_id, timeout=10)
    for update in updates:
        next_update_id = update.update_id + 1
        if update.message and update.message.text:
            logger.info("Found message %s!", update.message.text)
            await update.message.reply_text('Хәерле иртә!')
        return next_update_id
    return update_id


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
