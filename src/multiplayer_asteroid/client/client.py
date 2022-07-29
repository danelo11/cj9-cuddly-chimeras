"""Module."""
import logging
from dataclasses import dataclass
from queue import Empty, SimpleQueue

import pyglet
from pyglet.window import key

from multiplayer_asteroid.client.player import PlayerClient
from multiplayer_asteroid.utils import State


@dataclass
class AsteroidClientState(State):
    """Asteroid Client State."""

    score: int = 0
    num_asteroids: int = 3
    player_lives: int = 3


class AsteroidClient():
    """Asteroid Client."""

    def __init__(self):
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
        self.keyboard = key.KeyStateHandler()
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
            """On draw."""
            self.game_window.clear()
            self.main_batch.draw()
            self.counter.draw()

    def init(self):
        """Init the game."""
        self.score = 0
        self.score_label.text = "Score: " + str(self.score)
        self.num_asteroids = 3
        self.player_ship = PlayerClient(x=400, y=300, batch=self.main_batch)
        self.game_objects = [self.player_ship]
        self.game_window.push_handlers(self.keyboard)
        self.event_stack_size += 1

    def update_state(self, dt):
        """Update the game state."""
        try:
            new_state = self.state_queue.get(block=False)
            if new_state:
                if 'Player' in new_state:
                    self.player_ship.update(new_state['Player'])
                # parse state into game objects states
                # update state of game objects
        except Empty:
            pass
        if self.keyboard[key.X]:
            # TODO: send action to server
            logging.info("X pressed")
            ...
        if self.keyboard[key.SPACE]:
            # TODO: send action to server
            logging.info("SPACE pressed")
            ...
        # TODO complete this with the rest of the actions
        ...


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")
    client = AsteroidClient()
    # Start it up!
    client.run()
    client.init()
    pyglet.clock.schedule_interval(client.update_state, 1/120.0)
    pyglet.app.run()


if __name__ == "__main__":
    main()
