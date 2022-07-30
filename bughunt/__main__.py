"""Main game."""
from bughunt import logging_setup
from bughunt.clientside.client import main as client_main
from bughunt.serverside.server import main as server_main


def main():
    logging_setup()
    # run the server in main thread
    server_main()
    # threading.Thread(target=server_main, daemon=True).start()
    # run the client in a separate thread
    client_main()


if __name__ == "__main__":
    main()
