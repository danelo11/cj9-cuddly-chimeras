"""Module."""
import asyncio
import json
import logging
import random
import select
from dataclasses import dataclass
from queue import SimpleQueue

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

    def __init__(self, host: str, port: int):
        self.state_queue = SimpleQueue()
        self.action_queue = SimpleQueue()
        self.name: int = random.randrange(1, 1e6)
        self.host = host
        self.port = port

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

    def network_thread(self, dt: float):
        """Network thread."""
        ready = select.select([ws.conn], [], [], 0)
        if ready[0]:
            ws.net_recv()

        for network_event in ws.ws.events():
            if isinstance(network_event, Message):
                logging.info(network_event.data)
                self.state_queue.put(network_event.data)
            elif isinstance(network_event, CloseConnection):
                ws.setup(self.host, self.port)
            elif isinstance(network_event, Ping):
                ws.net_send(ws.ws.send(Pong(network_event.payload)))
            else:
                logging.warn(f"Unknown network event: {network_event}")


def main():
    """Main function."""
    logging_setup()
    logging.info("Main.")
    Resources()
    host, port = ('localhost', 8766)
    ws.setup(host, port)
    ws.send(json.dumps({"type": "name", "data": "player_pos"}))
    client = BugHuntClient(host, port)
    client.run()
    client.init()

    pyglet.clock.schedule_interval(client.update_state, 1/120.0)
    pyglet.clock.schedule_interval(client.network_thread, 1/60)
    pyglet.app.run()
    ws.close()


if __name__ == "__main__":
    main()
