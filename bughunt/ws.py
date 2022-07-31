import socket
import ssl
from typing import Generator

import certifi
from wsproto import Event, WSConnection
from wsproto.connection import ConnectionType
from wsproto.events import AcceptConnection, CloseConnection, Request

RECEIVE_BYTES = 4096

ctx = ssl.create_default_context(cafile=certifi.where())


class WebSocketClient:
    """A client wrapper for wsproto"""

    def __init__(self, host: str, port: int, target: str = "/") -> None:
        # All functions are disabled when the client is closed
        self.__disabled = False

        # Create the socket
        self.conn = socket.create_connection((host, port))
        if port == 443:
            self.conn = ctx.wrap_socket(self.conn, server_hostname=host)

        # Create the WebSocket connection
        self.ws = WSConnection(ConnectionType.CLIENT)

        # Send the handshake request
        self.send(Request(host=host, target=target))
        self.recv()

        # Receive the accept response
        for event in self.ws.handshake.events():
            if isinstance(event, AcceptConnection):
                break

    def send(self, out_data: bytes) -> None:
        """Send data to the server."""
        if self.__disabled:
            return

        # Send the data
        self.conn.send(self.ws.send(out_data))

    def recv(self) -> None:
        """Receive data from the server. To get the data, loop through self.events()."""
        if self.__disabled:
            raise

        # Receive the data
        in_data = self.conn.recv(RECEIVE_BYTES)

        # Parse the data
        if not in_data:
            self.ws.receive_data(None)
        else:
            self.ws.receive_data(in_data)

    def events(self) -> Generator[Event, None, None]:
        """A generator that yields pending events."""
        yield from self.ws.events()

    def close(self) -> None:
        """Close the connection."""
        if self.__disabled:
            return

        # Close the connection
        self.send(CloseConnection(code=1000, reason="Connection Closed."))

        # Receive the close response and close the socket
        self.recv()
        self.conn.shutdown(socket.SHUT_WR)
        self.recv()

        # Disable all functions
        self.__disabled = True
