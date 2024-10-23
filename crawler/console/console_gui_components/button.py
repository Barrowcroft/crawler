#  The Button class provides a basic button component.

from typing import Callable

import pygame

from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.show_text import show_text


class Button(Base):
    """Button

    The Button class provides a basic button component.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The Button class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the Button class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise Button.

        self.rect: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.callback: Callable[[], None]
        self.text: str = ""
        self.disabled: bool = False

        self.background_flag: bool = False
        self.button_colour: tuple[int, int, int] = (0, 0, 0)

        #  Initialise the offset used when checking for click and hover collision.

        self.x_adjust: int = 0
        self.y_adjust: int = 0

    def handleMouseEvent(self, event: pygame.event.Event, x_adjust: int = 0, y_adjust: int = 0) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.

        Args:
            event (pygame.event.Event): event to handle.
        """

        #  If the button is disabled exit immed.

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

        Check if a mouse clicks occurs in Button rectangle.

        Args:
            event (pygame.event.Event): mouse event
        """

        #  If mouse click collides with button rectangle call the callback method.
        #  Play the button sound if the options require it.

        if self.disabled is True:
            return

        if event.button == 1:
            _button_rect = pygame.rect.Rect(
                (
                    self.rect[0] + x_adjust,
                    self.rect[1] + y_adjust,
                    self.rect[2],
                    self.rect[3],
                )
            )
            if _button_rect.collidepoint(event.pos):
                if layout_config.button_sound_flag is True:
                    layout_config.button_sound.play()
                self.background_flag = False
                self.callback()

    def checkHover(
        self, event: pygame.event.Event, x_adjust: int = 0, y_adjust: int = 0
    ):
        """checkHover

        Check if a mouse motion occurs in Button rectangle.

        Args:
            event (pygame.event.Event): mouse event
        """

        #  If the position of the mouse collides with the button rectangle invert the buttons colours,
        #  and show the background.

        _button_rect = pygame.rect.Rect(
            (
                self.rect[0] + x_adjust,
                self.rect[1] + y_adjust,
                self.rect[2],
                self.rect[3],
            )
        )

        if _button_rect.collidepoint(event.pos):
            self.background_flag = True
        else:
            self.background_flag = False

    def update_button(
        self,
        rect: tuple[int, int, int, int],
        callback: Callable[[], None],
        text: str = "NOP",
        disabled: bool = False,
    ) -> None:
        """update_button

        Updates the Button parameters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the Button.
            callback (Callable[[], None]): method to call when Button is clicked.
            text (str): the text to display in the Button. Defaults to "NOP".
            disabled (bool): indicates if the button is disabled. Defalults to False.
        """
        #  Save parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.callback: Callable[[], None] = callback
        self.text: str = text
        self.disabled: bool = disabled

        #  Select colour; if the button is disabled it will have muted colour.

        self.button_colour: tuple[int, int, int] = layout_config.colour
        if disabled is True:
            self.button_colour = layout_config.muted_colour
            self.background_flag = False

        #  Update Base superclass.

        super().update_base(
            rect,
            colour=self.button_colour,
            background_flag=self.background_flag,
            corner_radius=5,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the Button class.

        Args:
            display (pygame.Surface): display on which to render.
        """
        #  Render the Base superclass.

        super().render(display)

        #  Draw the text.

        show_text(display, self.text, self.rect, layout_config.font, self.button_colour)
