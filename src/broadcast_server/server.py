from abc import ABC, abstractmethod
import asyncio
from typing import Dict, Set
import websockets
import json


class Connection:
    def __init__(self, ws: websockets.ServerConnection, username: str) -> None:
        self.ws = ws
        self.username = username


class IConnectionManager(ABC):
    @abstractmethod
    async def register(self, conn: Connection) -> None:
        pass

    @abstractmethod
    async def unregister(self, conn: Connection) -> None:
        pass

    @abstractmethod
    async def broadcast(self, msg: Dict) -> None:
        pass


class ConnectionManager(IConnectionManager):
    def __init__(self, clients: Set[Connection]) -> None:
        self._conns: Set[Connection] = clients

    async def register(self, conn: Connection) -> None:
        self._conns.add(conn)
        msg = {
            "type": "system",
            "message": f"Пользователь {conn.username} присоединился. Участников в чате: {len(self._conns)}",
        }
        await self.broadcast(msg)

    async def unregister(self, conn: Connection) -> None:
        self._conns.remove(conn)
        msg = {
            "type": "system",
            "message": f"Пользователь {conn.username} отсоединился. Участников в чате: {len(self._conns)}",
        }
        await self.broadcast(msg)

    async def broadcast(self, msg: Dict) -> None:
        if not self._conns:
            return
        data = json.dumps(msg, ensure_ascii=False)
        await asyncio.gather(
            *[conn.ws.send(data) for conn in list(self._conns)],
            return_exceptions=True,
        )


class BroadcastServer:
    def __init__(self, host: str, port: int, manager: IConnectionManager) -> None:
        self._host = host
        self._port = port
        self._manager = manager

    async def _handler(self, ws: websockets.ServerConnection) -> None:
        try:
            data = await ws.recv()
            obj = json.loads(data)
            user = obj.get("user")
        except Exception:
            await ws.close()
            return

        conn = Connection(ws, user)
        await self._manager.register(conn)

        try:
            async for msg in ws:
                data = json.loads(msg)
                if data["type"] == "chat":
                    resp = {"type": "chat", "user": user, "message": data["message"]}
                    await self._manager.broadcast(resp)
        except websockets.exceptions.ConnectionClosed:
            print("Соединение закрыто")
        finally:
            await self._manager.unregister(conn)

    async def start(self) -> None:
        srv = await websockets.serve(self._handler, self._host, self._port)
        print(f"Сервер запущен на ws://{self._host}:{self._port}")
        await srv.wait_closed()
