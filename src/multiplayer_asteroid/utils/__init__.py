"""Module."""
import logging
from dataclasses import dataclass


class State:
    """State."""

    # TODO serialize this class
    # TODO deserialize this class
    ...


@dataclass
class SpriteState:
    """Sprite State."""

    rotation: float = 0.
    x: int = 0
    y: int = 0

    def as_tuple(self):
        """As tuple."""
        return (self.x, self.y, self.rotation)


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")


if __name__ == "__main__":
    main()
