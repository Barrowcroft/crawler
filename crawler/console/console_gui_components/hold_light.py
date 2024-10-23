#  The HoldLight class provides a a basic light component.
#  The HoldLight has two lines of text.

import pygame

import crawler.constants as c
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.get_light_colour import get_light_colour
from crawler.console.console_tools.show_light_text_two_lines import (
    show_light_text_two_lines,
)


class HoldLight(Base):
    """HoldLight

    The HoldLight class provides a a basic light component.
    The HoldLight has two lines of text.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The HoldLight class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the HoldLight class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise HoldLight variables.

        self.rect: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.texts: tuple[str, str] = ("", "")
        self.light_colour: tuple[int, int, int] = c.BLACK

    def update_hold_light(
        self,
        rect: tuple[int, int, int, int],
        texts: tuple[str, str] = ("NOP", "NOP"),
        level: int = 0,
        percent: int = 0,
        status: str = "ONLINE",
        occupied: bool = False,
        personnel: bool = True,
        index: int = 0,
        max: int = 0,
        blink_flag: bool = False,
    ) -> None:
        """update_hold_light

        Updates the HoldLight parameters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the HoldLight.
            texts (tuple[str, str]): the texts to display in the HoldLight. Defaults to ("NOP", "NOP").
            level (int): the level (aka. colour) of the HoldLight. Defaults to 0.
            percent (int): the percent of the HoldLight. Defaults to 0.
            status (int): the status of the HoldLight. Defaults to "ONLINE".
            occupied (bool): indicates if the HoldLight represents an occupied slot. Defaults to True.
            personnel (bool): indicates if the HoldLight represents a personnel slot. Defaults to True.
            index (int): index of HoldLight - last one may have curved corners.
            max (int): maximum number of lights.
            blink_flag (bool): indicates if the HoldLight is in blink_flag cycle. Defaults to False.
        """
        #  Save parameters.

        self.rect = rect
        self.texts = texts

        #  Get the light colour. The danger colour will be shown during the blink cycle
        #  if the location is occupied and the health is down to zero.
        #  Otherwsie select a colour based on the health of the item or person.

        if ((percent == 0) and (occupied is True)) and blink_flag is False:
            self.light_colour: tuple[int, int, int] = layout_config.danger_colour
        else:
            self.light_colour = get_light_colour(
                level,
                blink_flag,
            )

        #  Check the text. Either showing the staus of the item or person,
        #  or indicating that the location is empty.

        if blink_flag is False:
            if status != "OK":
                self.texts = (status, "")

        if occupied is False:
            if personnel is True:
                self.texts = ("Unoccupied", "")
            else:
                self.texts = ("Unused", "")

        #  If the particular location is at the bottom of the list
        #  then the options may require it to have rounded bottom corners.

        if index == max - 1:
            _bootom_left: int = layout_config.corner_radius
            _bottom_right: int = layout_config.corner_radius
        else:
            _bootom_left: int = 0
            _bottom_right: int = 0

        #  Update Base superclass.

        super().update_base(
            rect,
            self.light_colour,
            bottom_left_corner_radius=_bootom_left,
            bottom_right_corner_radius=_bottom_right,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the HoldLight class.

        Args:
            display (pygame.Surface): display on which to render.
        """
        #  Render the superclass.

        super().render(display)

        #  Draw the text.

        show_light_text_two_lines(
            display,
            self.texts,
            self.rect,
            layout_config.font,
            self.light_colour,
        )
