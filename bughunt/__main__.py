import select

import numpy as np
import pyglet
from wsproto.events import CloseConnection, Message

from bughunt import logging_setup, ws

window = pyglet.window.Window(
    caption="Hello, World!",
)
batch = pyglet.graphics.Batch()

player = pyglet.shapes.Rectangle(
    width=50, height=50,
    x=window.width / 2, y=window.height / 2,
    batch=batch,
)
player_speed = np.zeros((2,), dtype=float)
pixels_per_second = 500

# host, port = "ws.ifelse.io", 80
# host, port = "dopad.herokuapp.com", 80
host, port = "dopad.herokuapp.com", 443


@window.event
def on_draw():
    window.clear()
    batch.draw()


def update(dt):
    if np.linalg.norm(player_speed) > 0:
        tmp = player_speed / np.linalg.norm(player_speed) * pixels_per_second * dt
        player.x += tmp[0]
        player.y += tmp[1]

        if player.x < 0:
            player.x = 0
        if player.x > window.width - player.width:
            player.x = window.width - player.width
        if player.y < 0:
            player.y = 0
        if player.y > window.height - player.height:
            player.y = window.height - player.height

        ws.send(str(player.x) + "," + str(player.y))


def network_update(_dt):
    ready = select.select([ws.conn], [], [], 0)
    if ready[0]:
        ws.net_recv()

    for network_event in ws.ws.events():
        if isinstance(network_event, Message):
            print(network_event.data)
        elif isinstance(network_event, CloseConnection):
            ws.setup(host, port)


@window.event
def on_key_press(symbol, modifiers):
    match symbol:
        case pyglet.window.key.W:
            player_speed[1] += 1
        case pyglet.window.key.S:
            player_speed[1] -= 1
        case pyglet.window.key.D:
            player_speed[0] += 1
        case pyglet.window.key.A:
            player_speed[0] -= 1


@window.event
def on_key_release(symbol, modifiers):
    match symbol:
        case pyglet.window.key.W:
            player_speed[1] -= 1
        case pyglet.window.key.S:
            player_speed[1] += 1
        case pyglet.window.key.D:
            player_speed[0] -= 1
        case pyglet.window.key.A:
            player_speed[0] += 1


def main():
    logging_setup()
    ws.setup(host, port)
    ws.send('{"type": "name", "data": "123"}')

    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.clock.schedule_interval(network_update, 1/60)
    pyglet.app.run()

    ws.close()


if __name__ == "__main__":
    main()
