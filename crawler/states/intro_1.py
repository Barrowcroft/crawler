#  The Intro game state.

import sys

import pygame  # type: ignore
import pygame.event  # type: ignore

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.show_text_block import show_text_block
from crawler.narrative import GAME_INTRO_TEXT_1
from crawler.states.state import State


class Intro_1(State):
    """Intro

    Args:
        State: this subclasses State.
    """

    @property
    def nextState(self) -> str:
        """nextState

        Gets the next game state.

        Returns:
            str: the next game state.
        """
        return self._nextState

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(self) -> None:
        """__init__

        Initialises the game state.

        """
        self._nextState: str = ""
        self._done: bool = False

        #  Layout the screen.

        self.background_rect: tuple[int, int, int, int] = c.SCREEN_BACKGROUND_RECT
        self.background: Base = Base()

        self.panel_rect: tuple[int, int, int, int] = c.SCREEN_PANEL_RECT
        self.panel: Base = Base()

        #  Start ambient soundtrack.

        if layout_config.ambient_sound_flag is True:
            layout_config.ambient_sound.play(loops=-1)

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.

        Args:
            event (pygame.event.Event): event to handle.
        """

        if event.type == pygame.KEYDOWN:

            if layout_config.key_sound_flag is True:
                layout_config.key_sound.play()

            _keys = pygame.key.get_pressed()
            if _keys[pygame.K_ESCAPE]:
                self._done = True
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                self._done = True

    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        ...

    def update(self, dt: float) -> None:
        """udate

        Updates the class.

        Args:
            dt (float): delta time
        """

        self.background.update_base(
            self.background_rect,
            colour=layout_config.colour,
            background_flag=layout_config.background_flag,
            frame_flag=layout_config.frame_flag,
        )
        self.panel.update_base(
            self.panel_rect,
            colour=layout_config.colour,
            background_flag=False,
            frame_flag=True,
            corner_radius=layout_config.corner_radius,
            bar=True,
        )

    def render(self, display: pygame.Surface, actualFPS: float) -> None:  # type: ignore
        """render

        Renders the class.

        Args:
            display (pygame.event.Event): display on which to render.
            actualFPS (float): actual frames per second.
        """

        self.background.render(display)
        self.panel.render(display)

        show_text_block(
            display,
            GAME_INTRO_TEXT_1,
            self.panel_rect,
            layout_config.large_font,
            layout_config.colour,
        )

    def checkDone(self) -> bool:
        """checkDone

        Checks if the current state is completed.

        Returns:
            bool: true if completed.
        """
        if self._done:
            self._nextState = c.GAME_INTRO_2
        return self._done
