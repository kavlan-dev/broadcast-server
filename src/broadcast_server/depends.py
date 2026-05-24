from typing import Set
from broadcast_server.client import CliClient
from broadcast_server.server import BroadcastServer, Connection, ConnectionManager

_conns: Set[Connection] = set()


def get_connections_set() -> Set[Connection]:
    return _conns


def get_connection_manager(conns: Set[Connection]) -> ConnectionManager:
    return ConnectionManager(conns)


def get_broadcast_server(
    host: str, port: int, manager: ConnectionManager
) -> BroadcastServer:
    return BroadcastServer(host, port, manager)


def get_cli_client(host: str, port: int, username: str) -> CliClient:
    return CliClient(host, port, username)
