import select

import pyglet
import ws
from wsproto.events import CloseConnection, Message

window = pyglet.window.Window(
    caption="Hello, World!",
)
batch = pyglet.graphics.Batch()

player = pyglet.shapes.Rectangle(
    width=50, height=50,
    x=window.width / 2, y=window.height / 2,
    batch=batch,
)
player_speed = [0, 0]
pixels_per_second = 500

host, port = "localhost", 8765


@window.event
def on_draw():
    window.clear()
    batch.draw()


def update(dt):
    player.x += player_speed[0] * dt
    player.y += player_speed[1] * dt

    if player.x < 0:
        player.x = 0
    if player.x > window.width - player.width:
        player.x = window.width - player.width
    if player.y < 0:
        player.y = 0
    if player.y > window.height - player.height:
        player.y = window.height - player.height

    ws.net_send(ws.ws.send(Message(str(player.x) + "," + str(player.y))))


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
            player_speed[1] += pixels_per_second
        case pyglet.window.key.S:
            player_speed[1] -= pixels_per_second
        case pyglet.window.key.D:
            player_speed[0] += pixels_per_second
        case pyglet.window.key.A:
            player_speed[0] -= pixels_per_second


@window.event
def on_key_release(symbol, modifiers):
    match symbol:
        case pyglet.window.key.W:
            player_speed[1] -= pixels_per_second
        case pyglet.window.key.S:
            player_speed[1] += pixels_per_second
        case pyglet.window.key.D:
            player_speed[0] -= pixels_per_second
        case pyglet.window.key.A:
            player_speed[0] += pixels_per_second


if __name__ == "__main__":
    ws.setup(host, port)

    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.clock.schedule_interval(network_update, 1/60)
    pyglet.app.run()

    ws.close()
