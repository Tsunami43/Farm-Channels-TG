from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Перезапустить бота"),
        BotCommand(command="view", description="Показать группы"),
        BotCommand(command="add", description="Добавить группу"),
        BotCommand(command="cancel", description="Отмена действия")
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())