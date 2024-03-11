import asyncpraw
from utils.loggers import get_logger
from typing import Optional


class Post:
    _id: str
    title: str
    text: str
    url: str

    def __init__(
        self,
        _id: str,
        title: str,
        text: str,
        url: str
    ):

        self._id = _id
        self.title = title
        self.text = text
        self.url = url


class Reddit:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        password: str,
        username: str,
        user_agent: str = "test"
    ):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.redirect_uri = redirect_uri

        self.logger = get_logger(__name__)
        

    async def check_news(self, target: str, last_data: list)-> Optional[Post]:
        response = None
        try:
            async with asyncpraw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            ) as reddit:

                target = target.replace("r/","")
                subreddit = await reddit.subreddit(target)
                async for submission in subreddit.new(limit=10):
                    if not submission.id in last_data:

                        response = Post(
                            submission.id,
                            submission.title,
                            submission.selftext,
                            submission.url
                        )
                        self.logger.info(f"Новый ивент в |{target}| id={submission.id}")
                        break
                
        except Exception as ex:
            self.logger.error(f"Ошибка |{target}|", exc_info=True)
        
        finally:
            return response