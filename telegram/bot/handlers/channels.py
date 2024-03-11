from aiogram import Router, F
from aiogram.types import Message

from telegram.bot.filters import MyChannel
from telegram.cheating import magic


router = Router()


@router.channel_post(MyChannel())
async def message_handler(message: Message):
    await magic.send_reaction(message.chat.id, message.message_id)