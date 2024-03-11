from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram.bot.filters import AdminFilter
from telegram.bot.states import EditChat
from telegram.bot.keyboards import paginator, Pagination, GetChat, menu_chat, Chat, yes_or_no
from telegram.owner import account
from telegram.cheating import magic

from database import db

from datetime import datetime
from os import remove


router = Router()


@router.callback_query(AdminFilter(), Pagination.filter(F.action.in_(["back", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: Pagination):
    
    chats = await db.get_chats()
    if isinstance(chats, list):
        if len(chats)>0:
            page = callback_data.page
            await call.message.edit_reply_markup(reply_markup=paginator(chats=chats, page=page))
        else:
            await call.message.edit_text(
                text="<u>У вас 0 чатов!</u>"
            )
    else:
        await call.message.edit_text(
            text="<i>ошибка получении данных из БД</i>"
        )

def edit_text(tup: tuple):
    return f"""🌐 {tup[2]}
    
link: {tup[4]}
username: <b>{tup[6]=='None' and tup[6] or "@"+tup[6]}</b>
id канала: <b>{tup[0]}</b>
id владельца: <b>{tup[1]}</b>
Источник канала: <b>{tup[5]}</b>

<b>*</b> <i>чтобы сделать канал публичный присвойте username каналу</i>

<b>*</b> <i>добавьте источник с Reddit, чтобы перенаправлять новости</i>
"""

@router.callback_query(AdminFilter(), GetChat.filter())
async def get_chat(call: CallbackQuery, callback_data: GetChat):
    chat = await db.get_chat(callback_data.chat_id)
    if chat:
        await call.message.edit_text(
            text=edit_text(chat),
            reply_markup=menu_chat(chat[0]),
            disable_web_page_preview=True
        )

    else:
        await call.message.answer('<b>Ошибка</b> чат не найден!')


@router.callback_query(AdminFilter(), F.data=='cancel_chat')
async def cancel_chat(call: CallbackQuery):
    chats = await db.get_chats()
    if isinstance(chats, list):
        if len(chats)>0:
            await call.message.edit_text(
                text="<u>Ваши чаты</u>:",
                reply_markup=paginator(chats=chats)
            )
        else:
            await call.message.edit_text(
                text="<u>У вас 0 чатов!</u>"
            )
    else:
        await call.message.edit_text(
            text="<i>ошибка получении данных из БД</i>"
        )


@router.callback_query(AdminFilter(), Chat.filter(F.action=="edit_photo"))
async def edit_photo(call: CallbackQuery, callback_data: Chat, state: FSMContext):
    await state.set_state(EditChat.photo)
    await state.update_data(chat_id=callback_data.chat_id)
    await call.message.edit_text(
        text="Для отмены /cancel\n\nДля изменения фото, <u>пришлите файл</u> соответствующего формата:"
    )


@router.message(AdminFilter(), EditChat.photo, F.photo)
async def photo_handler(message: Message, state: FSMContext, bot: Bot):
    
    data = await state.get_data()

    photo_path = f"{message.photo[-1].file_id}.jpg"
    await bot.download(
        message.photo[-1],
        destination=photo_path
    )

    if await account.set_chat_photo(
        data['chat_id'],
        photo_path
    ):
        await message.answer(
            "<b>Фото успешно изменено!</b>"
        )
    else:
        await message.answer(
            "<b>Ошибка фото не изменено!</b>"
        )

    remove(photo_path)
    await state.clear()


@router.callback_query(AdminFilter(), Chat.filter(F.action=="edit_username"))
async def edit_username(call: CallbackQuery, callback_data: Chat, state: FSMContext):
    await state.set_state(EditChat.username)
    await state.update_data(chat_id=callback_data.chat_id)
    await call.message.edit_text(
        text="Для отмены /cancel\n\nДля изменения username, пришлите ответ:"
    )


@router.message(AdminFilter(), EditChat.username, F.text)
async def username_handler(message: Message, state: FSMContext):
    
    data = await state.get_data()

    if await account.set_chat_username(
        data['chat_id'],
        message.text.strip()
    ):
        await message.answer(
            "<b>username успешно изменен!</b>"
        )
        if await db.change_chat(
            chat_id=data['chat_id'],
            key="username",
            value=message.text.strip()
        ):
            ...
        else:
            await message.answer(
                "<b>Ошибка при обновлении БД!</b>"
            ) 
    else:
        await message.answer(
            "<b>Ошибка username не изменен!</b>"
        )

    await state.clear()


@router.callback_query(AdminFilter(), Chat.filter(F.action=="edit_reddit"))
async def edit_reddit(call: CallbackQuery, callback_data: Chat, state: FSMContext):
    await state.set_state(EditChat.reddit)
    await state.update_data(chat_id=callback_data.chat_id)
    await call.message.edit_text(
        text="Для отмены /cancel\n\nДля изменения источника, пришлите ответ:"
    )


@router.message(AdminFilter(), EditChat.reddit, F.text)
async def reddit_handler(message: Message, state: FSMContext, bot: Bot):
    
    data = await state.get_data()

    if await account.invite_bot_to_channel(
        data['chat_id'],
        bot.id
    ):
        await message.answer(
            "<b>Источник успешно изменен!</b>"
        )
        if await db.change_chat(
            chat_id=data['chat_id'],
            key="reference",
            value=message.text.strip()
        ):
            await state.clear()
            channel = await db.get_chat(data['chat_id'])
            await magic.join_chat(channel[4])
        else:
            await message.answer(
                "<b>Ошибка при обновлении БД!</b>"
            )
            await state.clear()
    else:
        await message.answer(
            "<b>Ошибка, не смогли добавить бота!</b>"
        )
        await state.clear()


@router.callback_query(AdminFilter(), Chat.filter(F.action=="delete_chat"))
async def edit_reddit(call: CallbackQuery, callback_data: Chat):
    await call.message.edit_text(
        text=f"Вы действительнно хотите удалить из БД канал <b>{callback_data.chat_id}</b>",
        reply_markup=yes_or_no(callback_data.chat_id)
    )


@router.callback_query(AdminFilter(), Chat.filter(F.action=="yes_delete"))
async def edit_reddit(call: CallbackQuery, callback_data: Chat):
    if await db.delete_chat(callback_data.chat_id):

        await call.message.edit_text(
            text=f"Чат <b>{callback_data.chat_id}</b> - удален!"
        )

    else:
        await call.message.edit_text(
            text="Ошибка при удалении чата!"
        )


@router.callback_query(AdminFilter(), Chat.filter(F.action=="no_delete"))
async def edit_reddit(call: CallbackQuery, callback_data: Chat):
    chat = await db.get_chat(callback_data.chat_id)
    if chat:
        await call.message.edit_text(
            text=edit_text(chat),
            reply_markup=menu_chat(chat[0])
        )

    else:
        await call.message.answer('<b>Ошибка</b> чат не найден!')