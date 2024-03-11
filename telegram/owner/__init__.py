from .account import Account
from utils import config

account = Account(
    config.get("Telegram", "app_name"),
    int(config.get("Telegram", "api_id")),
    config.get("Telegram", "api_hash"),
    config.get("Telegram", "phone")
)