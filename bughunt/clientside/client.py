"""Module."""
import asyncio
import logging
import random
from dataclasses import dataclass
from select import select

import pyglet
from pyglet.window import key
from wsproto.events import CloseConnection, Message, Ping, Pong

from bughunt import logging_setup, ws
from bughunt.clientside.maze import Maze
from bughunt.clientside.player import PlayerClient
from bughunt.core.resources import Resources
from bughunt.utils import State


@dataclass
class BugHuntClientState(State):
    """BugHunt Client State."""

    score: int = 0
    num_bugs: int = 3
    player_lives: int = 3


class BugHuntClient():
    """BugHunt Client."""

    def __init__(self):
        self.state_queue = asyncio.Queue()
        self.action_queue = asyncio.Queue()
        self.name: int = random.randrange(1, 1e6)

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
        self.keyboard = key.KeyStateHandler()
        self.maze = Maze(x=415, y=280, batch=self.main_batch)
        self.player_ship = None
        self.player_lives = []
        self.score = 0
        self.num_bugs = 3
        self.game_objects = []
        # We need to pop off as many event stack frames as we pushed on
        # every time we reset the level.
        self.event_stack_size = 0

        @self.game_window.event
        def on_draw():
            """On draw."""
            self.game_window.clear()
            self.main_batch.draw()
            self.counter.draw()

    def init(self):
        """Init the game."""
        self.score = 0
        self.score_label.text = "Score: " + str(self.score)
        self.num_bugs = 3
        self.player_ship = PlayerClient(x=400, y=300, batch=self.main_batch)
        self.game_objects = [self.player_ship]
        self.game_window.push_handlers(self.keyboard)
        self.event_stack_size += 1

    def update_state(self, dt):
        """Update the game state."""
        try:
            new_state = self.state_queue.get_nowait()
            if new_state:
                if 'Player' in new_state:
                    self.player_ship.update(new_state['Player'])
                # parse state into game objects states
                # update state of game objects
        except asyncio.QueueEmpty:
            pass
        actions = {"player": self.name, "actions": []}
        if self.keyboard[key.X]:
            logging.info("X pressed")
            actions["actions"].append(key.X)
        if self.keyboard[key.SPACE]:
            logging.info("SPACE pressed")
            actions["actions"].append(key.SPACE)
        # TODO complete this with the rest of the actions
        ...
        if actions['actions']:
            self.action_queue.put_nowait(actions)
            logging.info(f"appending actions: {actions}, size: {self.action_queue.qsize()}")

    def network_update(self, _dt):
        """Network update."""
        global ws_client

        # Use select to not block the main thread
        if select([ws_client.conn], [], [], 0)[0]:
            ws_client.recv()

        for event in ws_client.events():
            if isinstance(event, Message):
                # TODO: parse events
                logging.info(f"Message received: {event.data}")
            elif isinstance(event, CloseConnection):
                # Reopen the connection
                ws_client.close()
                ws_client = ws.WebSocketClient(host, port)
            elif isinstance(event, Ping):
                # Send a pong reply
                ws_client.send(Pong(event.payload))
                logging.info(f"Ping received: {event.payload}")
            else:
                logging.warn(f"Unknown event: {event}")


def main():
    """Main function."""
    global ws_client, host, port

    logging_setup()
    logging.info("Main.")
    Resources()
    client = BugHuntClient()
    # Start the client
    client.run()
    client.init()

    # Setup the websocket client
    host, port = ('localhost', 8765)
    ws_client = ws.WebSocketClient(host, port)
    logging.info(f"Connecting to {host}:{port}")

    # Start the main loop
    fps = 120.0
    pyglet.clock.schedule_interval(client.network_update, 1/fps)
    pyglet.clock.schedule_interval(client.update_state, 1/fps)
    pyglet.app.run()


if __name__ == "__main__":
    main()
