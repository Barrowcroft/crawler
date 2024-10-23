#  The Light class provides a a basic light component.
#  The basic Light has one line of text.

import pygame

from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.get_light_colour import get_light_colour
from crawler.console.console_tools.show_light_text import show_light_text


class Light(Base):
    """Light

    The Light class provides a a basic light component.
    The basic light has one line of text.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The Light class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the Light class.
        """

        #  Initialise the Base superclass.

        super().__init__()

    def update_light(
        self,
        rect: tuple[int, int, int, int],
        text: str = "NOP",
        level: int = 0,
        blink_flag: bool = False,
    ) -> None:
        """updupdate_lightate

        Updates the Light parameters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the Light.
            text (str): the text to display in the Light. Defaults to "NOP".
            level (int): the level (aka. colour) of the Light. Defaults to 0.
            blink_flag (bool): indicates if the Light is in blink cycle. Defauls to False.
        """
        #  Save Light parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.text: str = text
        self.level: int = level
        self.blink_flag: bool = blink_flag

        #  Get the Light colour.

        self.light_colour: tuple[int, int, int] = get_light_colour(
            self.level,
            self.blink_flag,
        )

        #  Update Base superclass.

        super().update_base(rect, self.light_colour)

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the Light class.

        Args:
            display (pygame.Surface): display on which to render.
        """
        #  Render the Base superclass.

        super().render(display)

        #  Draw the text.

        show_light_text(
            display,
            self.text,
            self.rect,
            layout_config.font,
            self.light_colour,
        )
