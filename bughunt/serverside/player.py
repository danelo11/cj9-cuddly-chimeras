"""Player Serverside."""
import logging

import pyglet
from pyglet.window import key

from bughunt.core import resources
from bughunt.engine import physicalobject


class PlayerServer(physicalobject.PhysicalObject):
    """Physical object that responds to user input"""

    def __init__(self, *args, **kwargs):
        super(PlayerServer, self).__init__(img=resources.player_image, *args, **kwargs)

        # Create a child sprite to show when the ship is thrusting
        self.engine_sprite = pyglet.sprite.Sprite(img=resources.engine_image, *args, **kwargs)
        self.engine_sprite.visible = False

        # Set some easy-to-tweak constants
        self.thrust = 300.0
        self.rotate_speed = 200.0
        self.bullet_speed = 700.0

        # Player should not collide with own bullets
        self.reacts_to_bullets = False

        # Let pyglet handle keyboard events for us
        # self.key_handler = key.KeyStateHandler()
        # self.event_handlers = [self, self.key_handler]

    def update(self, dt, actions=None):
        """Update the player."""
        # Do all the normal physics stuff
        super(PlayerServer, self).update(dt)

        if key.X in actions:
            self.delete()

    def delete(self):
        """Delete the player."""
        # we have a child sprite which myst be deleted when this object
        # is deleted from batches, etc.
        self.engine_sprite.delete()
        super(PlayerServer, self).delete()


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")


if __name__ == "__main__":
    main()
