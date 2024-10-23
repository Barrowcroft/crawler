#  The State is the class from which all other game states are derived.

from abc import ABC, abstractmethod

import pygame  # type: ignore
import pygame.event  # type: ignore

import crawler.customlogger as customlogger


class State(ABC):
    """State

    The basic class for all game states.
    All other game states subclass this class.

    Args:
        ABC: this is an abstract base class.

    """

    #  PROPERTIES

    @property
    def nextState(self) -> str:
        """nextState

        Gets the next game state.

        Returns:
            str: the next game state.
        """
        return self._nextState

    #  GAME LOOP METHODS

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(self) -> None:
        """__init__

        Initialises the game state.

        """
        self._nextState: str = ""
        self._done: bool = False

    @abstractmethod
    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.
        Coordinates the handling of events by other classes.

        Args:
            event (pygame.event.Event): event to handle.
        """
        ...

    @abstractmethod
    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.
        Coordinates the handling of events by other classes.

        Args:
            event (pygame.event.Event): event to handle.
        """
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        """udate

        Updates the class.
        Coordinates the updating of all other classes.

        Args:
            dt (float): delta time
        """
        ...

    @abstractmethod
    def render(self, display: pygame.Surface) -> None:  # type: ignore
        """render

        Renders the class.
        Coordinates the rendering of all other classes.

        Args:
            display (pygame.event.Event): display on which to render.
            actualFPS (float): actual frames per second.
        """
        ...

    @abstractmethod
    def checkDone(self) -> bool:
        """checkDone

        Checks if the current state is completed.

        Returns:
            bool: true if completed.
        """
        return self._done
