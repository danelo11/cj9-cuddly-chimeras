import asyncio

import websockets


async def handler(websocket):
    while True:
        msg = await websocket.recv()
        await websocket.send(msg)


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()


asyncio.run(main())
