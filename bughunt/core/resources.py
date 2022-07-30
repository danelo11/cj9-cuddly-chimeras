"""Resources."""
import pyglet


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


# Tell pyglet where to find the resources
pyglet.resource.path = ['..\\resources', '.\\resources']
pyglet.resource.reindex()
# Load the three main resources and get them to draw centered
player_image = pyglet.resource.image("player.png")
maze_img = pyglet.resource.image('maze.png')
center_image(player_image)
center_image(maze_img)
