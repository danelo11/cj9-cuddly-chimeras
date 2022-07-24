import pyglet
import websockets
import asyncio

window = pyglet.window.Window(
    caption = "Hello, World!",
)

label = pyglet.text.Label(
    "Hello, World!",
    x=window.width / 2, y=window.height / 2,
)


@window.event
def on_draw():
    window.clear()
    label.draw()


# def update(dt):
#     print(dt)


if __name__ == "__main__":
    # pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()
