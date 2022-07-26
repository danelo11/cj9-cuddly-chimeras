"""How to run asteroid game?

1. Open terminal and navigate to the directory containing the asteroid game 'src'.
2. $ python -m asteroid.asteroid
"""
import logging

import pyglet

from asteroid.game import asteroid, load, player


class AsteroidGame():
    """Asteroid game."""

    def __init__(self):
        ...

    def run(self):
        """Run the game."""
        self.game_window = pyglet.window.Window(800, 600)
        self.main_batch = pyglet.graphics.Batch()
        self.score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=self.main_batch)
        self.level_label = pyglet.text.Label(
            text="Version 5: It's a Game!",
            x=400,
            y=575,
            anchor_x='center',
            batch=self.main_batch
        )

        self.game_over_label = pyglet.text.Label(
            text="GAME OVER",
            x=400,
            y=-300,
            anchor_x='center',
            batch=self.main_batch,
            font_size=48
        )

        self.counter = pyglet.window.FPSDisplay(window=self.game_window)
        self.player_ship = None
        self.player_lives = []
        self.score = 0
        self.num_asteroids = 3
        self.game_objects = []
        # We need to pop off as many event stack frames as we pushed on
        # every time we reset the level.
        self.event_stack_size = 0

        @self.game_window.event
        def on_draw():
            self.game_window.clear()
            self.main_batch.draw()
            self.counter.draw()

    def init(self):
        """Init the game."""
        self.score = 0
        self.score_label.text = "Score: " + str(self.score)
        self.num_asteroids = 3
        self.reset_level(2)

    def reset_level(self, num_lives=2):
        """Reset the level."""
        # Clear the event stack of any remaining handlers from other levels
        while self.event_stack_size > 0:
            self.game_window.pop_handlers()
            self.event_stack_size -= 1

        for life in self.player_lives:
            life.delete()

        self.player_ship = player.Player(x=400, y=300, batch=self.main_batch)
        self.player_lives = load.player_lives(num_lives, self.main_batch)
        self.asteroids = load.asteroids(self.num_asteroids, self.player_ship.position, self.main_batch)
        self.game_objects = [self.player_ship] + self.asteroids

        # Add any specified event handlers to the event handler stack
        for obj in self.game_objects:
            for handler in obj.event_handlers:
                self.game_window.push_handlers(handler)
                self.event_stack_size += 1

    def update(self, dt):
        """Update the game."""
        self.player_dead = False
        self.victory = False

        # To avoid handling collisions twice, we employ nested loops of ranges.
        # This method also avoids the problem of colliding an object with itself.
        for i in range(len(self.game_objects)):
            for j in range(i + 1, len(self.game_objects)):

                obj_1 = self.game_objects[i]
                obj_2 = self.game_objects[j]

                # Make sure the objects haven't already been killed
                if not obj_1.dead and not obj_2.dead:
                    if obj_1.collides_with(obj_2):
                        obj_1.handle_collision_with(obj_2)
                        obj_2.handle_collision_with(obj_1)

        # Let's not modify the list while traversing it
        to_add = []

        # Check for win condition
        self.asteroids_remaining = 0

        for obj in self.game_objects:
            obj.update(dt)

            to_add.extend(obj.new_objects)
            obj.new_objects = []

            # Check for win condition
            if isinstance(obj, asteroid.Asteroid):
                self.asteroids_remaining += 1

        if self.asteroids_remaining == 0:
            # Don't act on victory until the end of the time step
            self.victory = True

        # Get rid of dead objects
        for to_remove in [obj for obj in self.game_objects if obj.dead]:
            if to_remove == self.player_ship:
                self.player_dead = True
            # If the dying object spawned any new objects, add those to the
            # game_objects list later
            to_add.extend(to_remove.new_objects)

            # Remove the object from any batches it is a member of
            to_remove.delete()

            # Remove the object from our list
            self.game_objects.remove(to_remove)

            # Bump the score if the object to remove is an asteroid
            if isinstance(to_remove, asteroid.Asteroid):
                self.score += 1
                self.score_label.text = "Score: " + str(self.score)

        # Add new objects to the list
        self.game_objects.extend(to_add)

        # Check for win/lose conditions
        if self.player_dead:
            # We can just use the length of the player_lives list as the number of lives
            if len(self.player_lives) > 0:
                self.reset_level(len(self.player_lives) - 1)
            else:
                self.game_over_label.y = 300
        elif self.victory:
            self.num_asteroids += 1
            self.player_ship.delete()
            self.score += 10
            self.reset_level(len(self.player_lives))


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")
    game = AsteroidGame()
    # Start it up!
    game.run()
    game.init()

    pyglet.clock.schedule_interval(game.update, 1/120.0)
    pyglet.app.run()


if __name__ == "__main__":
    main()
