"""Module."""
import asyncio
import json
import logging
import random
import threading
from dataclasses import dataclass
from typing import Callable

import pyglet
import websockets
from pyglet.window import key

from bughunt import logging_setup
from bughunt.clientside.maze import Maze
from bughunt.clientside.player import PlayerClient
from bughunt.core.resources import Resources
from bughunt.utils import State


@dataclass
class BugHuntClientState(State):
    """BugHunt Client State."""

    score: int = 0
    num_bugs: int = 3
    player_lives: int = 3


class BugHuntClient():
    """BugHunt Client."""

    def __init__(self):
        self.state_queue = asyncio.Queue()
        self.action_queue = asyncio.Queue()
        self.name: int = random.randrange(1, 1e6)

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
        self.keyboard = key.KeyStateHandler()
        self.maze = Maze(x=415, y=280, batch=self.main_batch)
        self.player_ship = None
        self.player_lives = []
        self.score = 0
        self.num_bugs = 3
        self.game_objects = []
        # We need to pop off as many event stack frames as we pushed on
        # every time we reset the level.
        self.event_stack_size = 0

        @self.game_window.event
        def on_draw():
            """On draw."""
            self.game_window.clear()
            self.main_batch.draw()
            self.counter.draw()

    def init(self):
        """Init the game."""
        self.score = 0
        self.score_label.text = "Score: " + str(self.score)
        self.num_bugs = 3
        self.player_ship = PlayerClient(x=400, y=300, batch=self.main_batch)
        self.game_objects = [self.player_ship]
        self.game_window.push_handlers(self.keyboard)
        self.event_stack_size += 1

    def update_state(self, dt):
        """Update the game state."""
        try:
            new_state = self.state_queue.get_nowait()
            if new_state:
                if 'Player' in new_state:
                    self.player_ship.update(new_state['Player'])
                # parse state into game objects states
                # update state of game objects
        except asyncio.QueueEmpty:
            pass
        actions = {"player": self.name, "actions": []}
        if self.keyboard[key.X]:
            logging.info("X pressed")
            actions["actions"].append(key.X)
        if self.keyboard[key.SPACE]:
            logging.info("SPACE pressed")
            actions["actions"].append(key.SPACE)
        # TODO complete this with the rest of the actions
        ...
        if actions['actions']:
            self.action_queue.put_nowait(actions)
            logging.info(f"appending actions: {actions}, size: {self.action_queue.qsize()}")

    async def handler(self, websocket, loop: asyncio.AbstractEventLoop):
        """Handler.

        Handles the websocket connection and retrieve and push to the queue.
        """
        # task_state = asyncio.Task(self.handle_state(websocket))
        # task_actions = asyncio.Task(self.handle_actions(websocket))
        logging.info("handling...")
        # consumer_task = asyncio.Task(self.handle_state(websocket), loop=loop)
        # producer_task = asyncio.Task(self.handle_actions(websocket), loop=loop)
        # logging.info(consumer_task)
        # logging.info(producer_task)
        # await loop.gather(self.handle_state(websocket), self.handle_actions(websocket))
        logging.info(f"asyncio running loop: {asyncio.events.get_running_loop()}, loop: {loop}")
        # state_future = asyncio.run_coroutine_threadsafe(self.handle_state(websocket), loop)
        # loop.call_soon_threadsafe(self.handle_state(websocket))
        # actions_future = asyncio.run_coroutine_threadsafe(self.handle_actions(websocket), loop)
        # try:
        #     loop.run_forever()
        # finally:
        #     loop.close()
        # done, futures = await asyncio.wait([state_future, actions_future], return_when=asyncio.FIRST_COMPLETED)
        task_state = asyncio.create_task(self.handle_state(websocket))
        task_actions = asyncio.create_task(self.handle_actions(websocket))
        asyncio.gather(task_state, task_actions)
        # logging.info( asyncio.all_tasks(loop=loop))

    async def handle_state(self, websocket):
        """Handle state.

        Handles the websocket connection and retrieve and push to the queue.
        """
        logging.info("waiting for state to receive...")
        async for msg_state in websocket:
            logging.info(f"client recv: {msg_state}")
            self.state_queue.put_nowait(msg_state)
        # try:
        #     msg_state = await websocket.recv()
        # except websockets.ConnectionClosedOK:
        #     logging.info("Connection closed")
        #     msg_state = None

        # parse msg_state?
        # self.state_queue.put(msg_state)

    async def handle_actions(self, websocket):
        """Handle actions."""
        logging.info(f"Waiting for actions to send..., {self.action_queue.qsize()}")
        while True:
            try:
                logging.info("getting action...")
                actions = await self.action_queue.get()
            except asyncio.QueueEmpty:
                continue
            if actions:
                logging.info("Sending actions: %s", actions)
                await websocket.send(json.dumps(actions))

        # while not self.action_queue.empty():
        #     try:
        #         actions = self.action_queue.get(block=False)
        #     except Empty:
        #         break
        #     if actions:
        #         logging.info("Sending actions: %s", actions)
        #         await websocket.send(json.dumps(actions))


def network_thread(handler: Callable, host: str, port: int):
    """Network thread."""
    async def handle_network(loop: asyncio.AbstractEventLoop):
        """Handle network."""
        logging.info("Connecting to %s:%s", host, port)
        async for websocket in websockets.connect(f"ws://{host}:{port}"):
            logging.info("Connected")
            try:
                task = loop.create_task(handler(websocket, loop))
                await task
            except websockets.ConnectionClosed:
                logging.info("Connection closed")
                task.cancel()
                continue
        logging.info("Disconnected")
    loop = asyncio.new_event_loop()
    # loop.set_debug(True)
    logging.info("starting network thread, loop: %s", loop)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(handle_network(loop))
    loop.run_forever()
    loop.close()


def main():
    """Main function."""
    logging_setup()
    logging.info("Main.")
    Resources()
    client = BugHuntClient()
    client.run()
    client.init()
    host, port = ('localhost', 8766)
    threading.Thread(target=network_thread, daemon=True, kwargs={
        "handler": client.handler,
        "host": host,
        "port": port
    }).start()
    pyglet.clock.schedule_interval(client.update_state, 1/120.0)
    pyglet.app.run()


if __name__ == "__main__":
    main()
