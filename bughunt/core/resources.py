"""Resources."""
import logging
import pathlib
from dataclasses import dataclass, field

import numpy as np
import pyglet
from PIL import Image


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


# Walls Polygons
Walls = list[list[tuple[int, int]]]


@dataclass
class Map:
    """Map.

    Map data.
    """

    array_data: np.array = field(default_factory=lambda: np.array([]))
    width: int = 0
    height: int = 0


class Resources():
    """Resources."""

    def __init__(self):
        self.resource_path = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.resource_path = self.resource_path / 'resources'
        self.image_path = self.resource_path / 'images'
        self.sound_path = self.resource_path / 'sounds'
        self.font_path = self.resource_path / 'fonts'
        self.music_path = self.resource_path / 'music'
        self.logger = logging.getLogger(__name__)
        logging.info(f"Resources: {self.resource_path}")
        pyglet.resource.path = [str(self.resource_path.absolute())]
        pyglet.resource.reindex()
        self.logger.info('Resources initialized')
        print(pyglet.resource._default_loader._script_home)
        print(pyglet.resource._default_loader._index)
        self.maze_img = pyglet.resource.image('maze.png')
        center_image(self.maze_img)

    def player_image(self):
        """Player image."""
        player_image = pyglet.resource.image('player.png')
        center_image(player_image)
        # player_image = pyglet.image.load('player.png')
        return player_image

    def load_map(self, map_filename: pathlib.Path) -> Map:
        """Load map.

        Loads a map image and transforms it to polygons in place of the walls.
        """
        image = Image.open(self.resource_path / map_filename)
        image = image.convert('RGBA')
        # image.show()
        self.logger.info(f"Map image: {image}")
        threshold = 100
        # Grayscale
        image_file = image.convert('L')
        # Threshold
        image_file = image_file.point(lambda p: 255 if p > threshold else 0)
        # To mono
        image_file = image_file.convert('1')
        im = np.array(image_file)
        map = Map(array_data=im, width=image.width, height=image.height)
        return map


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")
    resources = Resources()
    resources.load_map('maze.png')


if __name__ == "__main__":
    main()
