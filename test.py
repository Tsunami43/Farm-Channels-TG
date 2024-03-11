
import asyncio
from reddit import viewer, stream
from reddit.objects import Post

from utils import config


async def main():
    await stream.event_loop()
        
asyncio.run(main())