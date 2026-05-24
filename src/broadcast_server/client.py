import asyncio
import sys
import websockets
import json


class CliClient:
    def __init__(self, host: str, port: int, username: str) -> None:
        self.uri = f"ws://{host}:{port}"
        self.username = username
        self.ws = None

    async def recv(self, ws: websockets.ClientConnection):
        try:
            while True:
                msg = await ws.recv()
                try:
                    data = json.loads(msg)
                    if data["type"] == "chat":
                        print(f"\n{data['user']}: {data['message']}")
                    elif data["type"] == "system":
                        print(f"\nСистема: {data['message']}")
                    else:
                        print(f"\nПолучено: {msg}")
                    print("> ", end="", flush=True)
                except json.JSONDecodeError:
                    print(f"\nПолучено: {msg}")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"\nОшибка при получении сообщений: {e}")

    async def send(self, ws: websockets.ClientConnection):
        try:
            while True:
                msg = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                msg = msg.strip()
                if msg.lower() in ["exit", "выйти"]:
                    print("Завершение работы...")
                    break
                msg = json.dumps({"type": "chat", "message": msg}, ensure_ascii=False)
                await ws.send(msg)
        except websockets.exceptions.ConnectionClosed:
            print("\nСоединение с сервером закрыто")
        except Exception as e:
            print(f"\nОшибка при отправке сообщения: {e}")

    async def connect(self):
        try:
            async with websockets.connect(self.uri) as ws:
                self.ws = ws
                await ws.send(json.dumps({"user": self.username}))
                print(f"Подключено к {self.uri}")
                print(
                    "Введите сообщение для отправки. Для выхода введите 'выйти' или 'exit'"
                )
                recv_task = asyncio.create_task(self.recv(ws))
                send_task = asyncio.create_task(self.send(ws))
                _, pending = await asyncio.wait(
                    [recv_task, send_task], return_when=asyncio.FIRST_COMPLETED
                )
                for task in pending:
                    task.cancel()
        except Exception as e:
            print(f"Ошибка: {e}")
