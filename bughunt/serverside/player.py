"""Player Serverside."""
import logging

from pyglet.window import key


class PlayerServer:
    """Physical object that responds to user input"""

    def __init__(self, x: float = 0., y: float = 0.):
        # Set some easy-to-tweak constants
        self.thrust = 300.0
        self.x = x
        self.y = y

    def update(self, dt, actions=None):
        """Update the player."""
        # Do all the normal physics stuff
        super(PlayerServer, self).update(dt)
        # check for collisions with walls
        self.check_collisions_walls()
        if key.X in actions:
            self.delete()

    def delete(self):
        """Delete the player."""
        # we have a child sprite which myst be deleted when this object
        # is deleted from batches, etc.
        super(PlayerServer, self).delete()


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")


if __name__ == "__main__":
    main()
