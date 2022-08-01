"""Module."""
import logging

import pyglet

from bughunt.core.resources import Resources


class Maze(pyglet.sprite.Sprite):
    """Maze."""

    def __init__(self, *args, **kwargs):
        super(Maze, self).__init__(img=Resources().maze_img, *args, **kwargs)

    def update(self):
        """Update Maze"""
        pass


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")


if __name__ == "__main__":
    main()
