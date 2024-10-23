#  The Switch class provides a switch button component.

from typing import Callable

import pygame

from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.show_text import show_text


class Switch(Base):
    """Switch

    The Switch class provides a switch button component.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The Switch class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the Switch class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise Switch variables.

        self.background_flag: bool = False
        self.text: str = ""
        self.Switch_colour: tuple[int, int, int] = (0, 0, 0)

        self.x_adjust: int = 0
        self.y_adjust: int = 0

    def handleMouseEvent(self, event: pygame.event.Event, x_adjust: int = 0, y_adjust: int = 0) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.

        Args:
            event (pygame.event.Event): event to handle.
        """

        #  If the switch is disabled exit immed.

        if self.disabled is True:
            return

        #  Check for click and hover.

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.checkClick(event, x_adjust, y_adjust)

        if event.type == pygame.MOUSEMOTION:
            self.checkHover(event, x_adjust, y_adjust)

    def checkClick(
        self, event: pygame.event.Event, x_adjust: int = 0, y_adjust: int = 0
    ):
        """checkClick

        Check if a mouse clicks occurs in Switch rectangle.

        Args:
            event (pygame.event.Event): mouse event
        """

        #  If the button is disabled exit immed.

        if self.disabled is True:
            return

        #  If mouse click collides with Switch rectangle call the callback method.

        if event.button == 1:
            _Switch_rect = pygame.rect.Rect(
                (
                    self.rect[0] + x_adjust,
                    self.rect[1] + y_adjust,
                    self.rect[2],
                    self.rect[3],
                )
            )
            if _Switch_rect.collidepoint(event.pos):
                if layout_config.button_sound_flag is True:
                    layout_config.button_sound.play()
                self.background_flag = False
                self.callback()

    def checkHover(
        self, event: pygame.event.Event, x_adjust: int = 0, y_adjust: int = 0
    ):
        """checkHover

        Check if a mouse motion occurs in Switch rectangle.

        Args:
            event (pygame.event.Event): mouse event
        """

        #  If the button is disabled exit immed.

        if self.disabled is True:
            self.background_flag = False
            return

        #  If the position of the mouse collides with the Switch rectangle invert the Switchs colours.

        _Switch_rect = pygame.rect.Rect(
            (
                self.rect[0] + x_adjust,
                self.rect[1] + y_adjust,
                self.rect[2],
                self.rect[3],
            )
        )
        if _Switch_rect.collidepoint(event.pos):
            self.background_flag = True
        else:
            self.background_flag = False

    def update_switch(
        self,
        rect: tuple[int, int, int, int],
        callback: Callable[[], None],
        text: str = "",
        on: bool = True,
        disabled: bool = False,
    ) -> None:
        """update_Switch

        Updates the Switch parameters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the Switch.
            callback (Callable[[], None]): method to call when Switch is clicked.
            text (str): the text to display in the Switch. Defaults to "NOP".
            on (bool): indicates if the switch is set on. Defaults to True.
            disabled (bool): indicates if the switch is disabled. Defaults to False.
        """
        #  Save Switch parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.callback: Callable[[], None] = callback
        self.text: str = text
        self.on: bool = on
        self.disabled: bool = disabled

        #  Select colour.

        self.Switch_colour: tuple[int, int, int] = layout_config.colour
        if disabled is True:
            self.Switch_colour = layout_config.muted_colour

        #  Update Base superclass.

        super().update_base(
            rect,
            colour=self.Switch_colour,
            background_flag=self.on,
            corner_radius=5,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the Switch class.

        Args:
            display (pygame.Surface): display on which to render.
        """
        #  Render the Base superclass.

        super().render(display)

        #  Draw the text. If text is provided show that,
        #  otherwise show 'On' or 'Off' as appropriate.

        _text: str = ""
        if self.text != "":
            _text = self.text
        else:
            if self.on is True:
                _text = "On"
            else:
                _text = "Off"

        show_text(display, _text, self.rect, layout_config.font, self.Switch_colour)
