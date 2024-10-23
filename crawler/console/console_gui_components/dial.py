#  The Dial class provides a basic dial component.

import math

import pygame

from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.draw_dial import draw_dial
from crawler.console.console_tools.get_light_colour import get_light_colour


class Dial(Base):
    """Dial

    The Dial class provides a basic dial component.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The Dial class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the Dial class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise Dial variables.

        self.rect: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.text: str = ""
        self.level: int = 0
        self.percent: int = 0
        self.blink_flag: bool = False

        self.value: int = 0

    def update_dial(
        self,
        rect: tuple[int, int, int, int],
        text: str = "NOP",
        level: int = 0,
        percent: int = 0,
        blink_flag: bool = False,
    ) -> None:
        """update_dial

        Updates the Dial parameters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the Dial.
            text (str): the text to display in the Dial. Defaults to "NOP".
            level (int): the level (aka. colour) of the Dial. Defaults to 0.
            percent (int): the Dial percent value. Defaults to 0.
            blink_flag (bool): indicates if the Dial is in blink_flag cycle. Defauls to False.
        """
        #  Save parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.text: str = text
        self.level: int = level
        self.blink_flag: bool = blink_flag

        #  Store a new target value.

        if percent != self.percent:
            self.percent = percent

        #  So the pointer does not just jump to the new value.
        #  change the value incrementally until it reaches the target value.

        if self.value < self.percent:
            self.value += math.ceil((self.percent - self.value) / 5)

        if self.value > self.percent:
            self.value -= math.ceil((self.value - self.percent) / 5)

        #  Get the dial colour.

        self.light_colour: tuple[int, int, int] = get_light_colour(
            self.level,
            self.blink_flag,
        )

        #  Update superclass.

        super().update_base(rect, self.light_colour)

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the Dial class.

        Args:
            display (pygame.Surface): display on which to render.
        """
        #  Render the superclass.

        super().render(display)

        #  Draw the dial.

        draw_dial(
            display,
            self.rect,
            self.text,
            self.level,
            self.value,
            self.blink_flag,
        )
