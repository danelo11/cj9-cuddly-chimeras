"""Resources."""
import logging
import os
import pathlib

import pyglet


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


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

    def load_map(self):
        """Load map.

        Loads a map image and transforms it to polygons in place of the walls.
        """
        ...


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")
    pyglet.resource.path = ['.\\pygletexample\\resources']
    pyglet.resource.reindex()
    os.walk(pyglet.resource.path)


if __name__ == "__main__":
    main()
