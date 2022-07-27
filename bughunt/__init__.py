import functools
import json
import logging
import logging.config
from pathlib import Path

logger = logging.getLogger(__name__)


@functools.lru_cache()
def logging_setup(
    default_path: str = "logging.json",
    default_level: int = logging.DEBUG
) -> None:
    """Establishing logging configuration to prompt messages to the console.

    Args:
        default_path (str, optional): Configuration file name. Defaults to "logging.json".
        default_level (int, optional): Logging level. Defaults to logging.DEBUG.
    """
    path = Path(__file__).parent / default_path
    if path.exists():
        with path.open(mode="rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        logger.info(f"Logging configuration file: {path.absolute()}")
        logger.info("File-based logging configuration successfully created.")
    else:
        logging.basicConfig(level=default_level)
        logger.warning("Basic logging configuration successfully created.")


logging_setup()
