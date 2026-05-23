import asyncio
import signal
from typing import Set

import websockets
from websockets.asyncio.server import ServerConnection


class ChatServer:
    def __init__(self, clients: Set[ServerConnection]) -> None:
        self.clients = clients

    async def handler(self, ws: ServerConnection) -> None:
        self.clients.add(ws)
        try:
            async for msg in ws:
                for client in self.clients:
                    if client != ws:
                        await client.send(msg)
        finally:
            self.clients.remove(ws)

    async def start_server(self, host: str, port: int) -> None:
        async with websockets.serve(self.handler, host, port):
            stop = asyncio.get_running_loop().create_future()
            loop = asyncio.get_running_loop()
            loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
            loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
            await stop
