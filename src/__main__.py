import asyncio
import concurrent.futures

import pyglet
import websockets

window = pyglet.window.Window(
    caption="Hello, World!",
)

label = pyglet.text.Label(
    "Hello, World!",
    x=window.width / 2, y=window.height / 2,
)

vrs = {
    "label.text": label.text,
}


@window.event
def on_draw():
    window.clear()
    label.draw()


def update(_dt):
    label.text = vrs["label.text"]


async def networking():
    async with websockets.connect("wss://ws.ifelse.io") as websocket:
        await websocket.recv()  # Random "Request served by <ID>" message
        vrs["label.text"] += " YES"


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(lambda: asyncio.run(networking()))
        pyglet.clock.schedule_interval(update, 1/60)
        pyglet.app.run()
