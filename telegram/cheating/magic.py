from configparser import ConfigParser
from pyrogram import Client

from utils.loggers import get_logger

from typing import Union
import random
from asyncio import sleep


class Cheating:

    def __init__(self):
        self.work_dir = "telegram/cheating/"
        config = ConfigParser()
        config.read(self.work_dir+'accounts.ini')
        self.accounts=[]
        for section in config.sections():
            self.accounts.append(section)

        self.priorrity = False
        self.logger = get_logger(__name__)


    def motion(f):
        """ 
            Decorator for start- and end- session
        """
        async def _await(*args, **kwargs):
            while args[0].priorrity:
                await sleep(0.2)
            args[0].priorrity = True
            for account in (args[0].accounts):
                await f(*args, account)
            args[0].priorrity = False
            

        return _await


    @motion
    async def join_chat(self, chat_id: Union[int,str], *args):
        try:
            async with Client(self.work_dir+"sessions/"+args[0]) as app:
                await app.join_chat(chat_id)
                self.logger.info(f"{args[0]} - join chat")
        except Exception as ex:
            self.logger.error(f"{args[0]} - join chat", exc_info=True)


    @motion
    async def send_reaction(self, chat_id: Union[int,str], message_id: int, *args):
        reactions = ['👍','👏','🔥']
        try:
            async with Client(self.work_dir+"sessions/"+args[0]) as app:
                await app.read_chat_history(chat_id)
                await app.send_reaction(
                    chat_id,
                    message_id,
                    random.choice(reactions)
                )
                self.logger.info(f"{args[0]} - send reaction")
        except Exception as ex:
            self.logger.error(f"{args[0]} - send reraction", exc_info=True)
