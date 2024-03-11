from reddit import viewer
from reddit.objects import Post
from database import db
from telegram.owner import account
#from telegram.bot import send_to_channel

from asyncio import sleep


async def event_loop():
    await sleep(10)
    while True:
        await sleep(10)
        chats = await db.get_chats()
        for chat in chats:
            target = chat[5]
            if isinstance(target, str) and "r/" in target:
                last_data = [_[0] for _ in await db.get_posts(chat[0])]
                post = await viewer.check_news(target, last_data)
                if isinstance(post, Post):
                    text = f'<b>{post.title}</b>\n\n{post.text}\n\n<a href="{post.url}"><u>Сссылка на источник</u></a>'
                    await account.send_to_channel(chat[0],text)
                    await db.add_post(chat[0], post._id)
