"""Player Serverside."""
import logging

from pyglet.window import key

from bughunt.core.resources import Map


class PlayerServer:
    """Physical object that responds to user input"""

    def __init__(
        self,
        x: float = 0.,
        y: float = 0.,
        width: float = 0.,
        height: float = 0.,
        map: Map = None
    ):
        # Set some easy-to-tweak constants
        self.thrust = 300.0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.map = map

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

    def check_collisions_walls(self, x, y):
        """Check for collisions with walls."""
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > self.map.width - self.width:
            self.x = self.map.width - self.width
        if self.y > self.map.height - self.height:
            self.y = self.map.height - self.height


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")


if __name__ == "__main__":
    main()
