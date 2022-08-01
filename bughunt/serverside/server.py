"""Server."""
import asyncio
import json
import logging
import time
from typing import Callable

import websockets

from bughunt.core.resources import Map, Resources
from bughunt.serverside.player import PlayerServer


class BugHuntServer():
    """BugHunt Server."""

    def __init__(self, map: Map):
        self.action_queue = asyncio.Queue()
        self.state_queue = asyncio.Queue()
        self.map = map

    def run(self):
        """Run the game."""
        self.player_ship = None
        self.player_lives = []
        self.score = 0
        self.num_bugs = 3
        self.game_objects = []
        # We need to pop off as many event stack frames as we pushed on
        # every time we reset the level.
        self.event_stack_size = 0

    def init(self):
        """Init the game."""
        self.score = 0
        self.num_bugs = 3
        self.player_ship = PlayerServer(x=400, y=300)

    async def update(self, dt: float):
        """Update the game."""
        logging.debug(f"queue size: {self.action_queue.qsize()}")
        try:
            new_actions = self.action_queue.get_nowait()
            if new_actions:
                if 'Player' in new_actions:
                    self.player_ship.update(new_actions['Player'])
                # parse state into game objects states
                # update state of game objects
        except asyncio.QueueEmpty:
            pass
        # TODO: update game objects from the new actions
        # TODO: create new states for the game objects

    async def consumer_handler(self, websocket):
        """Consumer handler."""
        logging.info("consumer_handler")
        async for msg_actions in websocket:
            logging.info(f"Server recv: {msg_actions}")
            actions = json.loads(msg_actions)
            await self.action_queue.put(actions)

    async def producer_handler(self, websocket):
        """Producer handler."""
        logging.info("producer_handler")
        while True:
            logging.info("getting state...")
            new_state = await self.state_queue.get()
            if new_state:
                logging.info("Sending state: %s", new_state)
                await websocket.send(
                    json.dumps({"Player": [self.player_ship.x, self.player_ship.y]})
                )

    async def handler(self, websocket):
        """Handler.

        Handles the websocket connection and retrieve and push to the queue.
        Server receives actions from the client and sends the new state to the
        client.
        """
        logging.info(f"New connection from {websocket.id}")
        await asyncio.gather(
            self.consumer_handler(websocket),
            self.producer_handler(websocket)
        )


async def periodic(t: float, func: Callable):
    """Periodic function.

    Runs the function every t seconds approximately.
    """
    # Setup some variables
    update_task = None
    start_timer = None
    scheduled_tasks = set()

    while await asyncio.sleep(t, result=True):
        if update_task:
            update_task.exception()
            update_task.cancel()

        # Measure the time it takes to loop
        end_timer = time.monotonic() if start_timer else None
        time_elapsed = end_timer - start_timer if end_timer else 0.0
        logging.debug('periodic update %.2f', time_elapsed)

        # Schedule the next update
        update_task = asyncio.create_task(func(time_elapsed))
        scheduled_tasks.add(update_task)
        update_task.add_done_callback(scheduled_tasks.discard)

        start_timer = time.monotonic()


async def async_main(server, host: str = "localhost", port: int = 8766):
    """Async main."""
    task = asyncio.create_task(periodic(0.1, server.update))
    try:
        async with websockets.serve(server.handler, host, port):
            await asyncio.Future()
    finally:
        logging.info("Closing the GameServer loop")
        task.cancel()


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")
    map = Resources().load_map("maze.png")
    server = BugHuntServer(map=map)
    server.run()
    server.init()

    asyncio.run(async_main(server), debug=True)
    # threading.Thread(target=network_thread, daemon=True, kwargs={"handler": server.handler}).start()


if __name__ == "__main__":
    main()
