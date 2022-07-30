"""Server."""
import asyncio
import logging
import threading
from queue import Empty, SimpleQueue
from typing import Callable

import pyglet
import websockets

from bughunt.serverside.player import PlayerServer


class AsteroidServer():
    """Asteroid Server."""

    def __init__(self):
        self.action_queue = SimpleQueue()
        self.state_queue = SimpleQueue()

    def run(self):
        """Run the game."""
        self.game_window = pyglet.window.Window(800, 600)
        self.main_batch = pyglet.graphics.Batch()
        self.score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=self.main_batch)
        self.level_label = pyglet.text.Label(
            text="Version 5: It's a Game!",
            x=400,
            y=575,
            anchor_x='center',
            batch=self.main_batch
        )

        self.game_over_label = pyglet.text.Label(
            text="GAME OVER",
            x=400,
            y=-300,
            anchor_x='center',
            batch=self.main_batch,
            font_size=48
        )

        self.counter = pyglet.window.FPSDisplay(window=self.game_window)
        self.player_ship = None
        self.player_lives = []
        self.score = 0
        self.num_asteroids = 3
        self.game_objects = []
        # We need to pop off as many event stack frames as we pushed on
        # every time we reset the level.
        self.event_stack_size = 0

        @self.game_window.event
        def on_draw():
            # here we want to send the state of the game to the client
            self.game_window.clear()
            self.main_batch.draw()
            self.counter.draw()

    def init(self):
        """Init the game."""
        self.score = 0
        self.score_label.text = "Score: " + str(self.score)
        self.num_asteroids = 3
        self.player_ship = PlayerServer(x=400, y=300, batch=self.main_batch)

    def update(self, dt):
        """Update the game."""
        try:
            new_actions = self.action_queue.get(block=False)
            if new_actions:
                if 'Player' in new_actions:
                    self.player_ship.update(new_actions['Player'])
                # parse state into game objects states
                # update state of game objects
        except Empty:
            pass
        # TODO: update game objects from the new actions
        # TODO: create new states for the game objects

    async def handler(self, websocket):
        """Handler.

        Handles the websocket connection and retrieve and push to the queue.
        """
        while True:
            msg = await websocket.recv()
            logging.info(msg)
            # try:
            #     actions = self.action_queue.get(block=False)
            # except Empty:
            #     actions = None
            # try:
            #     new_state = self.state_queue.get(block=False)
            # except Empty:
            #     new_state = None
            await websocket.send(msg)


def network_thread(handler: Callable):
    """Network thread."""
    async def handle_network():
        """Handle network."""
        async with websockets.serve(handler, "localhost", 8765):
            await asyncio.Future()
    asyncio.run(handle_network())


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")
    server = AsteroidServer()
    server.run()
    server.init()
    threading.Thread(target=network_thread, daemon=True, kwargs={"handler": server.handler}).start()
    pyglet.clock.schedule_interval(server.update, 1/120.0)
    pyglet.app.run()
