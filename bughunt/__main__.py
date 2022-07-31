"""Main game."""
from multiprocessing import Process

from bughunt import logging_setup
from bughunt.clientside.client import main as client_main
from bughunt.serverside.server import main as server_main


def main():
    logging_setup()
    # run the server in main thread
    # server_main()
    p = Process(target=server_main)
    p.start()
    # p.join()
    # threading.Thread(target=server_main, daemon=True).start()
    # run the client in a separate thread
    try:
        client_main()
    finally:
        p.kill()


if __name__ == "__main__":
    main()
