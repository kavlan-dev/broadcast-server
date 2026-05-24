import asyncio
from broadcast_server.depends import (
    get_broadcast_server,
    get_cli_client,
    get_connection_manager,
    get_connections_set,
)
import argparse


def main():
    parser = argparse.ArgumentParser("broadcast-server")
    parser.add_argument("command", choices=["start", "connect"])
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=8765)
    parser.add_argument("--username", default="anonymous")
    args = parser.parse_args()

    if args.command == "start":
        conns = get_connections_set()
        manager = get_connection_manager(conns)
        srv = get_broadcast_server(args.host, args.port, manager)

        asyncio.run(srv.start())
    elif args.command == "connect":
        client = get_cli_client(args.host, args.port, args.username)
        try:
            asyncio.run(client.connect())
        except KeyboardInterrupt:
            print("\nКлиент остановлен пользователем")


if __name__ == "__main__":
    main()
