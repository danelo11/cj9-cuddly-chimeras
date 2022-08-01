"""Phisical Object."""
import itertools
import logging

import pyglet

from bughunt import utils as util


class PhysicalObject(pyglet.sprite.Sprite):
    """A sprite with physical properties such as velocity"""

    def __init__(self, collisions=None, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)

        # Set collisions
        if collisions is None:
            collisions = []

        # Check if the collisions are convex polygons
        i = 0
        while i < len(collisions):
            if not util.is_convex(collisions[i]):
                logging.error(f"Collision polygon is not convex: {collisions[i]}")
                collisions.pop(i)
            else:
                i += 1

        # Set the convex collision polygons
        self._collisions = [(i[0], i[1]) for i in collisions]

        # In addition to position, we have velocity
        self.velocity_x, self.velocity_y = 0.0, 0.0

        # List of new objects to go in the game_objects list
        self.new_objects = []

        # Tell the game handler about any event handlers
        # Only applies to things with keyboard/mouse input
        self.event_handlers = []

    @property
    def collisions(self):
        """Getter for collisions."""
        return [
            [
                (i[0] + self.x + self.anchor_x, i[1] + self.y + self.anchor_y)
                for i in _collision
            ]
            for _collision in self._collisions
        ]

    def update(self, dt):
        """This method should be called every frame."""
        # Update position according to velocity and time
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def collides_with(self, other_object):
        """Determine if this object collides with another."""
        # Check if the other object is also a PhysicalObject
        if not isinstance(other_object, PhysicalObject):
            logging.error(f"Trying to check collision with non-PhysicalObject: {other_object}")
            return False

        # Loop through all of this and other object's collisions
        for collision, other_collision in itertools.product(self.collisions, other_object.collisions):
            # Check if the two polygons overlap
            if util.convex_polygons_overlap(collision, other_collision):
                return True

        return False


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")


if __name__ == "__main__":
    main()
