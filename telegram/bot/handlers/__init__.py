from .commands import router as router_commands
from .add_chat import router as router_add_chat
from .view_chats import router as router_view_chats
from .channels import router as router_channels

routers = [
    router_commands,
    router_add_chat,
    router_view_chats,
    router_channels
]