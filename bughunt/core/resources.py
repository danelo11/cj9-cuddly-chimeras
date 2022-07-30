"""Resources."""
import logging
import os

import pyglet


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


# Tell pyglet where to find the resources
print(pyglet.resource._default_loader._script_home)
print(pyglet.resource._default_loader._index)
pyglet.resource.path = ['..\\resources']
pyglet.resource.reindex()
print(pyglet.resource._default_loader._index)
# Load the three main resources and get them to draw centered
player_image = pyglet.resource.image("player.png")
maze_img = pyglet.resource.image('maze.png')
center_image(player_image)
center_image(maze_img)


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")
    pyglet.resource.path = ['.\\pygletexample\\resources']
    pyglet.resource.reindex()
    os.walk(pyglet.resource.path)


if __name__ == "__main__":
    main()
