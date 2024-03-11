from aiogram.filters import BaseFilter
from aiogram.types import Message

from database import db

class AdminFilter(BaseFilter):
    def __init__(self):
        self.admins = [6423473194, "atticd"]

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admins or message.from_user.username in self.admins


class MyChannel(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await db.get_chat(message.chat.id)!=None
