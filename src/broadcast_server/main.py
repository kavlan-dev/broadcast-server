import argparse
import asyncio

from broadcast_server.depends import get_chat_client, get_chat_server


def main() -> None:
    parser = argparse.ArgumentParser(prog="broadcast-server")
    sub = parser.add_subparsers(dest="cmd")

    s = sub.add_parser("start")
    s.add_argument("--host", default="localhost")
    s.add_argument("--port", type=int, default=8765)

    c = sub.add_parser("connect")
    c.add_argument("--host", default="localhost")
    c.add_argument("--port", type=int, default=8765)

    args = parser.parse_args()

    if args.cmd == "start":
        server = get_chat_server()
        print("Сервер запущен")
        asyncio.run(server.start_server(args.host, args.port))
    elif args.cmd == "connect":
        uri = f"ws://{args.host}:{args.port}"
        try:
            client = get_chat_client()
            print("Вы подключились к серверу")
            asyncio.run(client.run_client(uri))
        except KeyboardInterrupt:
            pass
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
