from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage

from telegram.bot.handlers import routers
from utils import config
from telegram.bot.ui_commands import set_bot_commands

from typing import Union


bot = Bot(token=config.get("Telegram", "bot_token"), parse_mode="HTML")

async def run():

    dp = Dispatcher(storage=MemoryStorage())
    await bot.delete_webhook(drop_pending_updates=True) 
    dp.include_routers(*routers)
    await set_bot_commands(bot)

    try:
        print("Бот запущен...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


async def send_to_channel(chat_id: Union[int,str], text: str):
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        disable_web_page_preview=True
    )