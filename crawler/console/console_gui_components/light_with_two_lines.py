#  The LightWithTwoLines class provides a light component with two lines of text.


import pygame

from crawler.config import layout_config
from crawler.console.console_gui_components.light import Light
from crawler.console.console_tools.show_light_text_two_lines import (
    show_light_text_two_lines,
)


class LightWithTwoLines(Light):
    """LightWithTwoLines

    The LightWithTwoLines class provides a light component with two lines of text.

    Args:
        Light: The LightWithTwoLines class subclasses the Light class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the LightWithTwoLines class.
        """

        #  Initialise the Light superclass.

        super().__init__()

    def update_light_with_two_lines(
        self,
        rect: tuple[int, int, int, int],
        texts: tuple[str, str] = ("NOP", "NOP"),
        level: int = 0,
        blink_flag: bool = False,
    ) -> None:
        """update_light_with_two_lines

        Updates the class parameters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the LightWithTwoLines.
            texts (tuple[str, str]): the texts to display in the LightWithTwoLines. Defaults to ("NOP", "NOP").
            level (int): the level (aka. colour) of the LightWithTwoLines. Defaults to 0.
            blink_flag (bool): indicates if the LightWithTwoLines is in blink cycle. Defauls to False.
        """
        # Save LightWithTwoLines parameters.

        self.texts: tuple[str, str] = texts

        #  Update Light superclass.

        super().update_light(
            rect,
            "",
            level,
            blink_flag,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the LightWithTwoLines class.

        Args:
            display (pygame.Surface): display on which to render.
        """
        #  Render the Light superclass.

        super().render(display)

        #  Draw the text.

        show_light_text_two_lines(
            display,
            self.texts,
            self.rect,
            layout_config.font,
            self.light_colour,
        )
