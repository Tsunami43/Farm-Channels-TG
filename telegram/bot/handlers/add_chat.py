from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from telegram.bot.filters import AdminFilter
from telegram.bot.states import AddGroup
from telegram.owner import account

from database import db


router = Router()


@router.message(AdminFilter(), AddGroup.title, F.text)
async def title_handler(message: Message, state: FSMContext):
    await state.set_state(AddGroup.description)
    await state.update_data(title=message.text)
    await message.answer(
        text="Для отмены /cancel\n\nВведите описание канала:"
    )


@router.message(AdminFilter(), AddGroup.description, F.text)
async def description_handler(message: Message, state: FSMContext, bot: Bot):
    msg = await message.answer(
        text="Запускаем процесс создания канала!"
    )

    data = await state.get_data()
    channel = await account.create_channel(
        title=data['title'],
        description=message.text
    )

    if channel:
        await bot.edit_message_text(
            "<b>Канал создан!</b>",
            chat_id=message.from_user.id,
            message_id=msg.message_id
        )
        if await db.add_chat(
            chat_id=channel.chat_id,
            owner_id=account.id,
            name=data['title'],
            description=message.text,
            link=channel.link
        ):
            await message.answer(
                text="<i>канал записан в БД</i>"
            )
        else:
            await message.answer(
                text="<i>ошибка записи канала в БД</i>"
            )
            
    else:
        await bot.edit_message_text(
            "Произошла <b>ошибка</b> при создании канала!",
            chat_id=message.from_user.id,
            message_id=msg.message_id
        )

    await state.clear()

