import asyncio

from pyrogram import Client

from utils import config


app_name = config.get("Telegram", "app_name")
api_id: int = int(config.get("Telegram", "api_id"))
api_hash: str = config.get("Telegram", "api_hash")
phone: str = config.get("Telegram", "phone")


async def main():
    async with Client(f"telegram/owner/{app_name}", api_id, api_hash, phone_number=phone) as app:
        me = await app.get_me()
        print(me)