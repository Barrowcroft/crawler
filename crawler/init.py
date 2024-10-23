#  The init.py file provides a number of initialisation methods used by the main.py file.

from typing import Any

import pygame  # type: ignore

import crawler.constants as c
import crawler.controller as controller
import crawler.customlogger as customlogger
from crawler.states.end import End
from crawler.states.intro_1 import Intro_1
from crawler.states.intro_2 import Intro_2
from crawler.states.main import Main
from crawler.states.splash import Splash
from crawler.states.state import State


@customlogger.log_trace(customlogger.Levels.INFO)
def getDisplay(gameTitle: str) -> pygame.Surface:  # type: ignore
    """getDisplay

    Initialises the pygame display.

    Args:
        gameTitle (str): title for screen.

    Returns:
        Surface: main game surface.
    """
    pygame.init()  # type: ignore
    pygame.mixer.init()  # type: ignore

    _flags = pygame.DOUBLEBUF | pygame.NOFRAME | pygame.SRCALPHA  # type: ignore

    _display: pygame.Surface = pygame.display.set_mode(c.SCREEN_SIZE, _flags)  # type: ignore
    pygame.display.set_caption(gameTitle)  # type: ignore

    return _display  # type: ignore


@customlogger.log_trace(customlogger.Levels.INFO)
def getClock() -> pygame.time.Clock:  # type: ignore
    """getClock

    Initialises the clock.

    Returns:
        Clock: the clock.
    """
    _clock: pygame.time.Clock = pygame.time.Clock()  # type: ignore

    return _clock  # type: ignore


@customlogger.log_trace(customlogger.Levels.INFO)
def getGameStates() -> dict[str, State]:
    """getGameStates

    Initialises the dictionary containing the game states.

    Returns:
        dict[str, State]: dictionary of game states.
    """
    _gamestates: dict[str, Any] = {
        c.GAME_SPLASH: Splash,
        c.GAME_INTRO_1: Intro_1,
        c.GAME_INTRO_2: Intro_2,
        c.GAME_MAIN: Main,
        c.GAME_END: End,
    }
    return _gamestates


@customlogger.log_trace(customlogger.Levels.INFO)
def getController(
    display: pygame.Surface,  # type: ignore
    clock: pygame.time.Clock,  # type: ignore
    gamestates: dict[str, State],
    startingState: str,
) -> controller.Controller:
    """getController

    Gets the game controller.

    """
    _controller: controller.Controller = controller.Controller(
        display, clock, gamestates, startingState
    )

    return _controller
