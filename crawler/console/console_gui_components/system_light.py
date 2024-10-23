#  The SystemLight class provides a light component.
#  The SystemLight has one line of text.

import pygame

from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.get_light_colour import get_light_colour
from crawler.console.console_tools.show_light_text import show_light_text

BLACK = (0, 0, 0)


class SystemLight(Base):
    """SystemLight

    The SystemLight class provides a light component.
    The basic light has one line of text.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The SystemLight class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the SystemLight class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise the SystemLight variables.

        self.rect: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.text: str = ""
        self.light_colour: tuple[int, int, int] = BLACK

    def update_system_light(
        self,
        rect: tuple[int, int, int, int],
        text: str = "NOP",
        level: int = 0,
        percent: int = 0,
        status: str = "ONLINE",
        blink_flag: bool = False,
    ) -> None:
        """update_light

        Updates the Light parameters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the SystemLight.
            text (str): the text to display in the SystemLight. Defaults to "NOP".
            level (int): the level (aka. colour) of the SystemLight. Defaults to 0.
            percent (int): the percent of the SystemLight. Defaults to 0.
            status (satr): the status of the SystemLight. Defaults to 0.
            blink_flag (bool): indicates if the SystemLight is in blink cycle. Defauls to False.
        """
        #  Save parameters.

        self.rect = rect
        self.text = text

        #  Get the light colour.

        if ((percent == 0) or (status != "ONLINE")) and blink_flag is False:
            self.light_colour: tuple[int, int, int] = layout_config.danger_colour
        else:
            self.light_colour = get_light_colour(
                level,
                blink_flag,
            )

        #  Check the text.

        if blink_flag is False:
            if status != "ONLINE":
                if status.startswith("OFFLINE"):
                    self.text = "OFFLINE"
                else:
                    self.text = status

        #  Update Base superclass.

        super().update_base(rect, self.light_colour)

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the Light class.

        Args:
            display (pygame.Surface): display on which to render.
        """
        #  Render the superclass.

        super().render(display)

        #  Draw the text.

        show_light_text(
            display,
            self.text,
            self.rect,
            layout_config.font,
            self.light_colour,
        )
