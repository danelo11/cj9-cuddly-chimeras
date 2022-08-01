import functools
import json
import logging
import logging.config
from pathlib import Path

logger = logging.getLogger(__name__)


@functools.lru_cache()
def logging_setup(
    config_file_name: str = "logging.json",
    default_level: int = logging.DEBUG
) -> None:
    """Establishing logging configuration to prompt messages to the console.

    Args:
        config_file_name (str, optional): Configuration file name. Defaults to "logging.json".
        default_level (int, optional): Logging level. Defaults to logging.DEBUG.
    """
    path = Path(__file__).parents[1] / 'config' / config_file_name
    if path.exists():
        with path.open(mode="rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        logger.info(f"Logging configuration file: {path.absolute()}")
        logger.info("File-based logging configuration successfully created.")
    else:
        logging.basicConfig(level=default_level)
        logger.warning("Basic logging configuration successfully created.")


def set_console_log_level(
    logger_level: int = logging.DEBUG,
    console_handler_level: int = logging.DEBUG,
) -> logging.Logger:
    """Change level of messages displayed through stdout.

    Args:
        logger_level (int, optional): logger level. Defaults to logging.DEBUG.
        console_handler_level (int, optional): the console handler level. Defaults to logging.INFO.

    Returns:
        logging.Logger: The output logger.
    """
    try:
        root: logging.Logger = logger.__dict__["parent"]
        _console_handler = [hand for hand in root.handlers if hand.name == "console"]
        try:
            console_handler = _console_handler[0]
            console_handler.setLevel(console_handler_level)
            root.setLevel(logger_level)
            logger.setLevel(logger_level)
        except IndexError:
            logger.warning(
                "Root logger has no console handler attached! "
                f"Can't set console handler level to {console_handler_level}"
            )

    except AttributeError:
        logger.warning(
            "No root logger found. "
            f"Can't set root logger level to {logger_level}.\n"
            f"logger.__dict__={logger.__dict__}"
        )
    return logger
