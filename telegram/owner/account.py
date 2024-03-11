from typing import Union, Optional
from asyncio import sleep

from pyrogram import Client, errors, enums
from pyrogram.types import Chat, ChatPrivileges

from utils.loggers import get_logger

class Channel:
    chat_id: int
    link: str

    def __init__(self, chat_id: int, link: str):
        self.chat_id = chat_id
        self.link = link


class Account:
    app_name: str
    api_id: int
    api_hash: str
    phone: str

    app: Client
    

    def __init__(
        self,
        app_name: str,
        api_id: int = None,
        api_hash: str = None,
        phone: str = None
    ):
        self.app = Client(
            "telegram/owner/"+app_name,
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone
        )
        self.app.set_parse_mode(enums.ParseMode.HTML)

        self.id: int = None
        self.priorrity = False
        self.logger = get_logger(__name__)


    def connection(f):
        """ 
            Decorator for start- and end- session
        """
        async def _await(*args, **kwargs):
            response = None
            try:
                while args[0].priorrity:
                    await sleep(0.2)
                args[0].priorrity = True
                async with args[0].app:
                    response = await f(*args, **kwargs)
                args[0].priorrity = False
            except Exception as ex:
                self.logger.error(f"{args[0].id}: ошибка connection", exc_info=True)
            finally:
                return response

        return _await


    async def check_owner(self)-> bool:
        response = False
        try:
            await self.app.connect()
            me = await self.app.get_me()
            self.id = me.id
            print(f"{self.id}: аккаунт подключен к серверу ТГ...")
            response = True
        except (
            errors.ActiveUserRequired,
            errors.AuthKeyInvalid,
            errors.AuthKeyPermEmpty,
            errors.AuthKeyUnregistered,
            errors.AuthKeyDuplicated,
            errors.SessionExpired,
            errors.SessionPasswordNeeded,
            errors.SessionRevoked,
            errors.UserDeactivated,
            errors.UserDeactivatedBan,
        ) as ex:
            print("|Ошибка|Проблема при подключении к серверу ТГ")
            self.logger.error(ex)
        except Exception as ex:
            print("|Неизвестная ошибка| Проблема при подключении к серверу ТГ")
            self.logger.error(ex)
        finally:
            await self.app.disconnect()
            return response


    @connection
    async def create_channel(
        self,
        title: str,
        description: str
    )-> Optional[Channel]:

        try:
            chat: Chat = await self.app.create_channel(
                title,
                description
            )
            async for link in self.app.get_chat_admin_invite_links(chat_id=chat.id, admin_id="me", limit=1):
                continue
            self.logger.info(f"{self.id}: создал канал |{title}| с описанием - {description}")
            return Channel(
                chat_id=chat.id,
                link=link.invite_link
            )
        except Exception as ex:
            self.logger.error(f"{self.id}: ошибка при создании канала |{title}| с описанием - {description}", exc_info=True)
            return None


    @connection
    async def set_chat_photo(
        self,
        chat_id: Union[int, str],
        photo_path: str
    )-> bool:

        try:
            if await self.app.set_chat_photo(chat_id, photo=photo_path):
                self.logger.info(f"{self.id}: обновлено фото в |{chat_id}|")
                return True
            else:
                self.logger.exception(f"{self.id}: вызвано исключение при смене фото в |{chat_id}|")
                return False
        except Exception as ex:
            self.logger.error(f"{self.id}: ошибка при смене фото в |{chat_id}|", exc_info=True)
            return False


    @connection
    async def set_chat_protected_content(
        self,
        chat_id: Union[int, str],
        enabled: bool
    )-> bool:
        """ 
            Set the chat protected content setting
        """
        try:
            if await self.app.set_chat_protected_content(chat_id, enabled):
                self.logger.info(f"{self.id}: защита контента в |{chat_id}| обновлена с {not enabled} на {enabled}")
                return True
            else:
                self.logger.exception(f"{self.id}: вызвано исключение при обновлении защиты контента в |{chat_id}|")
                return False
        except Exception as ex:
            self.logger.error(f"{self.id}: ошибка при обновлении защиты контента в |{chat_id}|", exc_info=True)
            return False


    @connection
    async def set_chat_username(
        self,
        chat_id: Union[int, str],
        username: str=None
    )-> bool:

        try:
            if await self.app.set_chat_username(chat_id, username):
                self.logger.info(f"{self.id}: юзернейм изменен в |{chat_id}| на {username}")
                return True
            else:
                self.logger.exception(f"{self.id}: вызвано исключение при смене юзернейма в |{chat_id}| на {username}")
                return False
        except Exception as ex:
            self.logger.error(f"{self.id}: ошибка при смене юзернейма в |{chat_id}| на {username}", exc_info=True)
            return False
    
    
    @connection
    async def invite_bot_to_channel(
        self,
        chat_id: Union[int, str],
        bot_id: Union[int, str]
    )-> bool:

        try:
            if await self.app.promote_chat_member(
                chat_id,
                bot_id,
                ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_promote_members=True,
                    can_change_info=True,
                    can_post_messages=True,
                    can_edit_messages=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    is_anonymous=True
                )
            ):
                self.logger.info(f"{self.id}: бот({bot_id}) добавлен в |{chat_id}|")
                return True
            else:
                self.logger.exception(f"{self.id}: вызвано исключение при добавлении бота({bot_id}) в |{chat_id}|")
                return False
        except Exception as ex:
            self.logger.error(f"{self.id}: ошибка при добавлении бота({bot_id}) в |{chat_id}|", exc_info=True)
            return False


    @connection
    async def send_to_channel(
        self,
        chat_id: Union[int, str],
        text: str
    )-> None:

        try:
            await self.app.send_message(chat_id, text)
            self.logger.info(f"{self.id}: сообщение отправлено в |{chat_id}|")
        except Exception as ex:
            self.logger.error(f"{self.id}: ошибка при отправки сообщения в |{chat_id}|", exc_info=True)