"""Server."""
import asyncio
import logging
import threading
from queue import Empty, SimpleQueue
from typing import Callable

import pyglet
import websockets

from bughunt.serverside.player import PlayerServer


class BugHuntServer():
    """BugHunt Server."""

    def __init__(self):
        self.action_queue = SimpleQueue()
        self.state_queue = SimpleQueue()

    def run(self):
        """Run the game."""
        self.player_ship = None
        self.player_lives = []
        self.score = 0
        self.num_bugs = 3
        self.game_objects = []
        # We need to pop off as many event stack frames as we pushed on
        # every time we reset the level.
        self.event_stack_size = 0

    def init(self):
        """Init the game."""
        self.score = 0
        self.num_bugs = 3
        self.player_ship = PlayerServer(x=400, y=300)

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
    server = BugHuntServer()
    server.run()
    server.init()
    threading.Thread(target=network_thread, daemon=True, kwargs={"handler": server.handler}).start()
    pyglet.clock.schedule_interval(server.update, 1/120.0)


if __name__ == "__main__":
    main()
