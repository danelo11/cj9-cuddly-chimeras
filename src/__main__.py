import select

import pyglet
from wsproto.events import CloseConnection, Message

import ws

window = pyglet.window.Window(
    caption="Hello, World!",
)
batch = pyglet.graphics.Batch()

label = pyglet.text.Label(
    "Hello, World!",
    x=window.width / 2, y=window.height / 2,
    batch=batch,
)

host, port = "localhost", 8765


@window.event
def on_draw():
    window.clear()
    batch.draw()


def update(_dt):
    pass  # Code


def network_update(_dt):
    ready = select.select([ws.conn], [], [], 0)
    if ready[0]:
        ws.net_recv()

    for network_event in ws.ws.events():
        if isinstance(network_event, Message):
            print(network_event.data)
        elif isinstance(network_event, CloseConnection):
            ws.setup(host, port)


if __name__ == "__main__":
    ws.setup(host, port)
    ws.net_send(ws.ws.send(Message("Hello, World!")))
    ws.net_send(ws.ws.send(Message("It works!")))

    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.clock.schedule_interval(network_update, 1/60)
    pyglet.app.run()

    ws.close()
