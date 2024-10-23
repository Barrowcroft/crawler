#  The LightWithThreeLines class provides a light component with three lines of text.


import pygame

from crawler.config import layout_config
from crawler.console.console_gui_components.light import Light
from crawler.console.console_tools.show_light_text_three_lines import (
    show_light_text_three_lines,
)


class LightWithThreeLines(Light):
    """LightWithThreeLines

    The LightWithThreeLines class provides a light component with Three lines of text.

    Args:
        Light: The LightWithThreeLines class subclasses the Light class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the LightWithThreeLines class.
        """

        #  Initialise the Light superclass.

        super().__init__()

    def update_light_with_three_lines(
        self,
        rect: tuple[int, int, int, int],
        texts: tuple[str, str, str] = ("NOP", "NOP", "NOP"),
        level: int = 0,
        blink_flag: bool = False,
    ) -> None:
        """update_light_with_three_lines

        Updates the class parameters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the LightWithThreeLines.
            texts (tuple[str, str, str]): the texts to display in the LightWithThreeLines. Defaults to ("NOP", "NOP", "NOP").
            level (int): the level (aka. colour) of the LightWithThreeLines. Defaults to 0.
            blink_flag (bool): indicates if the LightWithThreeLines is in blink cycle. Defauls to False.
        """
        # Save Light parameters.

        self.texts: tuple[str, str, str] = texts

        #  Update Light superclass.

        super().update_light(
            rect,
            "",
            level,
            blink_flag,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the LightWithThreeLines class.

        Args:
            display (pygame.Surface): display on which to render.
        """
        #  Render the Light superclass.

        super().render(display)

        #  Draw the text.

        show_light_text_three_lines(
            display,
            self.texts,
            self.rect,
            layout_config.font,
            self.light_colour,
        )
