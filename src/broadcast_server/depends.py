from typing import Set

from websockets import ServerConnection

from broadcast_server.client import ChatClient
from broadcast_server.server import ChatServer


clients: Set[ServerConnection] = set()


def get_chat_server() -> ChatServer:
    return ChatServer(clients)


def get_chat_client() -> ChatClient:
    return ChatClient()
