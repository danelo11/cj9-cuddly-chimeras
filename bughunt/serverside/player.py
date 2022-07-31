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
        self.thrust = 10.0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.map = map

    def update(self, dt, actions: dict = None):
        """Update the player."""
        if actions is None:
            return
        if 'left' in actions:
            x = self.x - self.thrust * dt
        if 'right' in actions:
            x = self.x + self.thrust * dt
        if 'up' in actions:
            y = self.y + self.thrust * dt
        if 'down' in actions:
            y = self.y - self.thrust * dt
        if 'a' in actions:
            x = self.x - self.thrust * dt
        if 'd' in actions:
            x = self.x + self.thrust * dt
        if 'w' in actions:
            y = self.y + self.thrust * dt
        if 's' in actions:
            y = self.y - self.thrust * dt
        # check for collisions with walls
        if self.check_collisions_walls(x, y):
            return
        if self.check_out_boundaries(x, y):
            return
        if key.X in actions:
            self.delete()

    def delete(self):
        """Delete the player."""
        # we have a child sprite which myst be deleted when this object
        # is deleted from batches, etc.
        super(PlayerServer, self).delete()

    def check_collisions_walls(self, x, y):
        """Check for collisions with walls."""
        if self.map.is_wall(x, y):
            return True
        return False

    def check_out_boundaries(self, x, y):
        """Check for collisions with boundaries."""
        if self.map.is_out_boundary(x, y):
            return True
        return False


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")


if __name__ == "__main__":
    main()
