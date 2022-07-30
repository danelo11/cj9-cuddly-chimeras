"""Module."""
import logging
from dataclasses import dataclass

import pyglet
from pyglet.window import key

from bughunt.core import resources
from bughunt.utils import SpriteState, State


@dataclass
class PlayerState(SpriteState, State):
    """Player State."""

    ...


class PlayerClient(pyglet.sprite.Sprite):
    """PlayerClient."""

    def __init__(self, *args, **kwargs):
        super(PlayerClient, self).__init__(img=resources.player_image, *args, **kwargs)
        self.state = PlayerState()
        # Let pyglet handle keyboard events for us
        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

    def update(self, new_state: PlayerState = None):
        """Update the player."""
        self.state = new_state
        super(PlayerClient, self).update(*self.state.as_tuple())
        if self.key_handler[key.X]:
            # send action to server
            logging.info("X pressed")
            ...


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")
    player_state = PlayerState(
        rotation=0.,
        x=0,
        y=0
    )
    print(player_state)


if __name__ == "__main__":
    main()
