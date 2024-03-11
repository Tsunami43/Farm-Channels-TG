import sqlite3, aiosqlite
from typing import Union, List, Tuple

from utils.loggers import get_logger


class Database:
    path_db: str


    def __init__(self, path_db: str = "database/db.db"):
        self.path_db = path_db
        conn = sqlite3.connect(
            self.path_db ,
            check_same_thread=False
        )
        curs = conn.cursor()
        curs.execute('''
            CREATE TABLE IF NOT EXISTS Chats (
                chat_id INTEGER PRIMARY KEY,
                owner_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                link TEXT NOT NULL,
                reference TEXT,
                username TEXT,
                members INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
        self.logger = get_logger(__name__)
        print("База даннных подключена ...")


    # async def create_table(self, chat_id: int)-> None:
    #     async with aiosqlite.connect(
    #         self.path_db,
    #         check_same_thread=False
    #     ) as db:

    #         await db.execute(f'''
    #             CREATE TABLE {chat_id} (
    #                 key TEXT NOT NULL
    #             )
    #         ''')
    #         await db.commit()


    async def add_chat(
        self,
        chat_id: int,
        owner_id: int,
        name: str,
        description: str,
        link: str,
        reference: str=None,
        username: str=None,
        members: int=0
    )-> bool:
        try:
            async with aiosqlite.connect(
                self.path_db,
                check_same_thread=False
            ) as db:

                await db.execute(f'''
                    INSERT INTO Chats (
                        chat_id,
                        owner_id,
                        name,
                        description,
                        link,
                        reference,
                        username,
                        members) 
                    VALUES ('{chat_id}', '{owner_id}', '{name}', '{description}', '{link}', '{reference}', '{username}', '{members}')
                ''')
                await db.execute(f'''
                    CREATE TABLE '{str(chat_id)}' (
                        key TEXT NOT NULL
                    )
                ''')
                await db.commit()

                self.logger.info(f"Создание чата |{chat_id}| с параметрами:\n"+
                    f"chat_id:{chat_id}\n"+
                    f"owner_id:{owner_id}\n"+
                    f"name:{name}\n"+
                    f"description:{description}\n"+
                    f"link:{link}\n"+
                    f"reference:{reference}\n"+
                    f"username:{username}\n"+
                    f"members:{members}\n"
                )
                return True

        except Exception as ex:
            self.logger.error(
                f"Ошибка создания чата |{chat_id}| с параметрами:\n"+
                f"chat_id:{chat_id}\n"+
                f"owner_id:{owner_id}\n"+
                f"name:{name}\n"+
                f"description:{description}\n"+
                f"link:{link}\n"+
                f"reference:{reference}\n"+
                f"username:{username}\n"+
                f"members:{members}\n",
                exc_info=True
            )
            return False


    async def get_chat(self, chat_id: int)-> Tuple:
        try:
            async with aiosqlite.connect(
                self.path_db,
                check_same_thread=False
            ) as db:

                    async with db.execute(f"""
                        SELECT * FROM Chats WHERE chat_id='{str(chat_id)}'
                    """) as curs:

                        self.logger.info(f"Получение чата |{chat_id}|")
                        return await curs.fetchone()

        except Exception as ex:
            self.logger.error(f"Ошибка получение чата |{chat_id}|", exc_info=True)
            return None

    async def get_chats(self)-> List[tuple]:
        try:
            async with aiosqlite.connect(
                self.path_db,
                check_same_thread=False
            ) as db:

                    async with db.execute("""
                        SELECT * FROM Chats
                    """) as curs:

                        self.logger.info(f"Получение списка чатов")
                        return await curs.fetchall()

        except Exception as ex:
            self.logger.error(f"Ошибка получения списка чатов", exc_info=True)
            return None


    async def change_chat(self, chat_id: int, key: str, value: Union[str, int])-> bool:
        try:
            async with aiosqlite.connect(
                self.path_db,
                check_same_thread=False
            ) as db:

                await db.execute(f"""
                    UPDATE Chats SET '{key}' = '{value}' WHERE chat_id='{chat_id}'
                """)
                await db.commit()

                self.logger.info(f"Изменение инфо о чате |{chat_id}|--> {key}:{value}")
                return True

        except Exception as ex:
            self.logger.error(f"Ошибка изменение инфо о чате |{chat_id}|--> {key}:{value}", exc_info=True)
            return False
    

    async def add_post(self, chat_id: int, value: str)-> bool:
        try:
            async with aiosqlite.connect(
                self.path_db,
                check_same_thread=False
            ) as db:

                await db.execute(f"""
                    INSERT INTO '{str(chat_id)}' (key) VALUES ('{value}')
                """)
                await db.commit()

                self.logger.info(f"Добавления поста в чат |{chat_id}|")
                return True

        except Exception as ex:
            self.logger.error(f"Ошибка добавления поста в чат |{chat_id}|", exc_info=True)
            return False


    async def get_posts(self, chat_id: int)-> List[tuple]:
        try:
            async with aiosqlite.connect(
                self.path_db,
                check_same_thread=False
            ) as db:

                    async with db.execute(f"""
                        SELECT * FROM '{str(chat_id)}'
                    """) as curs:

                        self.logger.info(f"Получения постов чата |{chat_id}|")
                        return await curs.fetchall()

        except Exception as ex:
            self.logger.error(f"Ошибка получения постов чата |{chat_id}|", exc_info=True)
            return None


    async def delete_chat(self, chat_id: int)-> bool:
        try:
            async with aiosqlite.connect(
                self.path_db,
                check_same_thread=False
            ) as db:

                await db.execute(f"""
                    DELETE FROM Chats WHERE chat_id='{chat_id}'
                """)
                await db.execute(f"""
                    DROP TABLE '{str(chat_id)}'
                """)
                await db.commit()

                self.logger.info(f"Чат |{chat_id}| удален")
                return True

        except Exception as ex:
            self.logger.error(f"Ошибка удаления чата |{chat_id}|", exc_info=True)
            return False