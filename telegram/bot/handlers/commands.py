from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from telegram.bot.filters import AdminFilter
from telegram.bot.states import AddGroup
from telegram.bot.keyboards import paginator

from database import db


router = Router()


@router.message(AdminFilter(), StateFilter(None), Command('start'))
async def start_handler(message: Message):
    await message.answer(
        text=
            f"Здравствуй{message.from_user.full_name==None and '' or ', <u>'+message.from_user.full_name+'</u>'}!\n\n"+
            "/start - <i>Перезапустить бота</i>\n\n"+
            "/view - <i>Список каналов</i>\n\n"+
            "/add - <i>Создать группу</i>\n\n"
    )


@router.message(AdminFilter(), StateFilter(None), Command('view'))
async def view_handler(message: Message):
    chats = await db.get_chats()
    if isinstance(chats, list):
        if len(chats)>0:
            await message.answer(
                text="<u>Ваши чаты</u>:",
                reply_markup=paginator(chats=chats)
            )
        else:
            await message.answer(
                text="<u>У вас 0 чатов!</u>"
            )
    else:
        await message.answer(
            text="<i>ошибка получении данных из БД</i>"
        )

@router.message(AdminFilter(), StateFilter(None), Command('add'))
async def add_handler(message: Message, state: FSMContext):
    await state.set_state(AddGroup.title)
    await message.answer(
        text=
            "Для отмены /cancel\n\nВведите название канала:"
    )


@router.message(AdminFilter(), Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="<b>Действие отменено!</b>"
    )