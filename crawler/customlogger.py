#  The custom logger provides a decorator to add logging code to any mehtod or function.

import enum
import logging
import os
from typing import Any, Callable

import crawler.constants as c

#  Set up logging levels.


class Levels(enum.Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


#  Set up logging file.

_filename = os.path.join(os.getcwd(), "crawler", f"{c.GAME_NAME}.log")

#  Set up the default logger.

logging.basicConfig(
    level=logging.DEBUG,
    filename=_filename,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def log_level(level: str) -> None:
    """log_level

    Sets the logging level for the default logger.

    Args:
        level (str): new logging level.
    """
    logger: logging.Logger = logging.getLogger()
    logger.setLevel(level)


def log_trace(level: Levels) -> Callable[..., Any]:
    """log_trace

    Decorates a function/method with logging code.

    Args:
        level (Levels): the logging level of the message.

    Returns:
        Callable[..., Any]: the decorated function/method.
    """

    def log_trace(func: Callable[..., Any]) -> Callable[..., Any]:

        def logged_func(*args: Any, **kwargs: Any):
            message: str = (
                f"Function '{func.__module__}' '{func.__name__}' with *args {args} and **kwargs {kwargs}."
            )
            log_message(message, level)
            return func(*args, **kwargs)

        return logged_func

    return log_trace


def log_message(message: str, level: Levels) -> None:
    """log_message

    Logs a message aqccording to the given loging level.

    Args:
        message (str): the message to log.
        level (Levels): the logging level of the message.
    """

    if level == Levels.DEBUG:
        logging.debug(message)
    if level == Levels.INFO:
        logging.info(message)
    if level == Levels.WARNING:
        logging.warning(message)
    if level == Levels.ERROR:
        logging.error(message)
    if level == Levels.CRITICAL:
        logging.critical(message)
