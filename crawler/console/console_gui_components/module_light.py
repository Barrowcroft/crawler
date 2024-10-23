#  The ModuleLight class provides a light component.
#  The ModuleLight has three lines of text.

from typing import Callable, Optional

import pygame

from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.get_light_colour import get_light_colour
from crawler.console.console_tools.show_light_text_three_lines import (
    show_light_text_three_lines,
)

BLACK = (0, 0, 0)


class ModuleLight(Base):
    """ModuleLight

    The ModuleLight class provides a light component.
    The ModuleLight has three lines of text.
    The ModuleLight also has a button-like area.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The ModuleLight class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the ModuleLight class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise ModuleLight variables.

        self.rect: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.texts: tuple[str, str, str] = ("", "", "")
        self.light_colour: tuple[int, int, int] = BLACK
        self.hover_flag: bool = False

        self.light_rect: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.button_rect: tuple[int, int, int, int] = (0, 0, 0, 0)

        self.selected: bool = False

        self.bot_right_corner_radius: int = 0

    def checkClick(
        self, event: pygame.event.Event, x_adjust: int = 0, y_adjust: int = 0
    ):
        """checkClick

        Check if a mouse clicks occurs in Button rectangle.

        Args:
            event (pygame.event.Event): mouse event
            x_adjust (int); adjustment to the x position for collision checking.
            y_adjust (int); adjustment to the y position for collision checking.
        """

        #  If mouse click collides with button rectangle call the callback method.

        if event.button == 1:

            #  Create collision rectange.

            _collision_rect = pygame.rect.Rect(
                (
                    self.button_rect[0] + x_adjust,
                    self.button_rect[1] + y_adjust,
                    self.button_rect[2],
                    self.button_rect[3],
                )
            )

            #  Check for collision, and if so invoke calback.

            if _collision_rect.collidepoint(event.pos):
                if layout_config.button_sound_flag is True:
                    layout_config.button_sound.play()
                self.hover_flag = False

                self.selected = not self.selected

                if self.action is not None:
                    self.action()

    def checkHover(
        self, event: pygame.event.Event, x_adjust: int = 0, y_adjust: int = 0
    ):
        """checkHover

        Check if a mouse motion occurs in Button rectangle.

        Args:
            event (pygame.event.Event): mouse event.
            x_adjust (int); adjustment to the x position for collision checking.
            y_adjust (int); adjustment to the y position for collision checking.
        """

        #  If the position of the mouse collides with the button set the hover flag,
        #  which will in turn set the background to show.

        #  Create collision rectange.

        _collision_rect = pygame.rect.Rect(
            (
                self.button_rect[0] + x_adjust,
                self.button_rect[1] + y_adjust,
                self.button_rect[2],
                self.button_rect[3],
            )
        )

        #  Set hover flag, to show background.

        if _collision_rect.collidepoint(event.pos):
            self.hover_flag = True
        else:
            self.hover_flag = False

    def update_module_light(
        self,
        rect: tuple[int, int, int, int],
        texts: tuple[str, str, str] = ("NOP", "NOP", "NOP"),
        level: int = 0,
        percent: int = 0,
        status: str = "ONLINE",
        occupied: bool = False,
        index: int = 0,
        max: int = 0,
        blink_flag: bool = False,
        action: Optional[Callable[[], None]] = None,
    ) -> None:
        """update_module_light

        Updates the ModuleLight parameters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the ModuleLight.
            texts (tuple[str, str, str]): the texts to display in the ModuleLight. Defaults to ("NOP", "NOP", "NOP").
            level (int): the level (aka. colour) of the ModuleLight. Defaults to 0.
            percent (int): the percent of the ModuleLight. Defaults to 0.
            status (int): the status of the ModuleLight. Defaults to "ONLINE".
            occupied (bool): indicates if the ModuleLight represents an occupied slot. Defauls to True.
            index (int): index of ModuleLight - last one may have curved corners.
            max (int): maximum number of lights.
            blink_flag (bool): indicates if the ModuleLight is in blink_flag cycle. Defauls to False.
            action (Optional[Callable[[], None]]): method to call whn button is pressd. Defaults to None.
        """
        #  Save parameters.

        self.rect = rect
        self.texts = texts
        self.action: Optional[Callable[[], None]] = action

        #  Calculate rects.

        if occupied is True:

            #  Light rect.

            self.light_rect: tuple[int, int, int, int] = (
                self.rect[0],
                self.rect[1],
                self.rect[2] - 24,
                self.rect[3],
            )

            #  Button rect.

            self.button_rect: tuple[int, int, int, int] = (
                self.rect[0] + self.rect[2] - 21,
                self.rect[1],
                21,
                self.rect[3],
            )

        else:
            self.light_rect = self.rect
            self.button_rect = (0, 0, 0, 0)

        #  Get the light colour. The danger colour will be shown during the blink cycle
        #  if the location is occupied and the health is down to zero.
        #  Otherwsie select a colour based on the health of the module.

        if (
            ((percent == 0) or status != "ONLINE")
            and (occupied is True)
            and blink_flag is False
        ):
            self.light_colour: tuple[int, int, int] = layout_config.danger_colour
        else:
            self.light_colour = get_light_colour(
                level,
                blink_flag,
            )

        #  Check the text. Either showing the staus of the module,
        #  or indicating that the location is empty.

        if blink_flag is False:
            if status != "ONLINE":
                if status.startswith("OFFLINE"):
                    self.texts = ("OFFLINE", "", "")
                else:
                    self.texts = (status, "", "")

        if occupied is False:
            self.texts = ("Unused", "", "")

        #  If the particular location is at the bottom of the list
        #  then the options may require it to have rounded bottom corners.

        if index == max - 1:
            _bottom_left: int = layout_config.corner_radius
            self.bot_right_corner_radius: int = layout_config.corner_radius
        else:
            _bottom_left: int = 0
            self.bot_right_corner_radius: int = 0

        #  Set the button state.

        if status == "ONLINE":
            self.selected = True
        else:
            self.selected = False

        #  Update Base superclass.

        super().update_base(
            self.light_rect,
            self.light_colour,
            bottom_left_corner_radius=_bottom_left,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the ModuleLight class.

        Args:
            display (pygame.Surface): display on which to render.
        """
        #  Render the superclass.

        super().render(display)

        #  Draw the text.

        show_light_text_three_lines(
            display,
            self.texts,
            self.light_rect,
            layout_config.font,
            self.light_colour,
        )

        #  Darw the button area.

        _button_text_colour: tuple[int, int, int] = self.light_colour

        if self.hover_flag is False:
            _width: int = 1
        else:
            _width = 0
            _button_text_colour = BLACK

        if self.selected is True:
            _width = 0

        pygame.draw.rect(
            display,
            self.light_colour,
            self.button_rect,
            _width,
            border_bottom_right_radius=self.bot_right_corner_radius,
        )
