from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class GetChat(CallbackData, prefix="get"):
    chat_id: int 


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


def paginator(chats: list, page: int = 0):
    
    builder = InlineKeyboardBuilder()
    limit = 10
    start_offset = page * limit 
    end_offset = start_offset + limit 
    for chat in chats[start_offset:end_offset]: 
        builder.row(
            InlineKeyboardButton(
                text=f"🌐 {chat[2]}",
                callback_data=GetChat(
                    chat_id=chat[0]
                ).pack()
            )
        )

    buttons_row = []  
    if page > 0:
        buttons_row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=Pagination(
                    action="back",
                    page=page - 1
                ).pack()
            )
        )
    if limit < len(chats):
        if end_offset < len(chats):
            buttons_row.append(
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=Pagination(
                        action="next",
                        page=page + 1
                    ).pack()
                )
            )
        else:
            buttons_row.append(
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=Pagination(
                        action="next",
                        page=0
                    ).pack()
                )
            )

    builder.row(*buttons_row)

    return builder.as_markup()


class Chat(CallbackData, prefix="edit"):
    action: str
    chat_id: int


def menu_chat(chat_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Изменить фото',
            callback_data=Chat(
                action='edit_photo',
                chat_id=chat_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Установить/изменить username',
            callback_data=Chat(
                action='edit_username',
                chat_id=chat_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Добавить/изменить источник',
            callback_data=Chat(
                action='edit_reddit',
                chat_id=chat_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Удалить канал из БД',
            callback_data=Chat(
                action='delete_chat',
                chat_id=chat_id
            ).pack()
        )
    )
    builder.row(InlineKeyboardButton(
        text='⬅️ Вернуться к списку каналов',
        callback_data='cancel_chat'
        )
    )
    return builder.as_markup()


def yes_or_no(chat_id):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Да',
            callback_data=Chat(
                action='yes_delete',
                chat_id=chat_id
            ).pack()
        ),
        InlineKeyboardButton(
            text='Нет',
            callback_data=Account(
                action='no_delete',
                chat_id=chat_id
            ).pack()
        )
    )

    return builder.as_markup()