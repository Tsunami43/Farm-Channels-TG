from .objects import Reddit
from utils import config

viewer = Reddit(
    client_id=config.get("Reddit","client_id"),
    client_secret=config.get("Reddit","client_secret"),
    redirect_uri=config.get("Reddit","redirect_uri"),
    password=config.get("Reddit","password"),
    username=config.get("Reddit","username")
)