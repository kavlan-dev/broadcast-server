import asyncio
import websockets
import sys
from websockets.asyncio.client import ClientConnection


class ChatClient:
    async def send_loop(self, ws: ClientConnection) -> None:
        loop = asyncio.get_running_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)
        while True:
            line = await reader.readline()
            if not line:
                break
            msg = line.decode().rstrip("\n")
            await ws.send(msg)

    async def recv_loop(self, ws: ClientConnection) -> None:
        try:
            async for msg in ws:
                print(msg)
        except websockets.ConnectionClosed:
            return

    async def run_client(self, uri: str) -> None:
        async with websockets.connect(uri) as ws:
            await asyncio.gather(self.send_loop(ws), self.recv_loop(ws))
