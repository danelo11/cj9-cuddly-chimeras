import socket
import ssl

import certifi
from wsproto import WSConnection
from wsproto.connection import ConnectionType
from wsproto.events import (
    AcceptConnection, BytesMessage, CloseConnection, Request, TextMessage
)

RECEIVE_BYTES = 4096

ctx = ssl.create_default_context(cafile=certifi.where())
conn = None
ws = None


def net_send(out_data: bytes) -> None:
    if ws is None or conn is None:
        raise Exception("setup() not run")

    conn.send(out_data)


def send(data: str | bytes) -> None:
    if ws is None or conn is None:
        raise Exception("setup() not run")

    if isinstance(data, str):
        net_send(ws.send(TextMessage(data)))
    elif isinstance(data, bytes):
        net_send(ws.send(BytesMessage(data)))
    else:
        raise Exception("send() only accepts str or bytes")


def net_recv() -> None:
    if ws is None or conn is None:
        raise Exception("setup() not run")

    in_data = conn.recv(RECEIVE_BYTES)
    if not in_data:
        ws.receive_data(None)
    else:
        ws.receive_data(in_data)


def close() -> None:
    global ws, conn
    if ws is None or conn is None:
        raise Exception("setup() not run")

    net_send(ws.send(CloseConnection(code=1000, reason="Connection Closed.")))
    net_recv()
    conn.shutdown(socket.SHUT_WR)
    net_recv()

    conn = None
    ws = None


def setup(host: str, port: int) -> None:
    global conn, ws
    conn = socket.create_connection((host, port))
    if port == 443:
        conn = ctx.wrap_socket(conn, server_hostname=host)

    ws = WSConnection(ConnectionType.CLIENT)
    net_send(ws.send(Request(host=host, target="/")))
    net_recv()
    for event in ws.handshake.events():
        if isinstance(event, AcceptConnection):
            break
