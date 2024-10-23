#  The CrawlerLight class provides a light component.
#  The CrawlerLight has three lines of text.

from typing import Callable, Optional

import pygame

from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.get_light_colour import get_light_colour
from crawler.console.console_tools.show_light_text_three_lines import (
    show_light_text_three_lines,
)
from crawler.console.console_tools.show_text import show_text

BLACK = (0, 0, 0)


class CrawlerLight(Base):
    """CrawlerLight

    The CrawlerLight class provides a light component.
    The CrawlerLight has three lines of text.
    The CrawlerLight also has a button-like area.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The CrawlerLight class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the CrawlerLight class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise CrawlerLight variables.

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

    def update_crawler_light(
        self,
        rect: tuple[int, int, int, int],
        texts: tuple[str, str, str],
        report: dict[str, int],
        selected: bool,
        blink_flag: bool = False,
        action: Optional[Callable[[], None]] = None,
    ) -> None:
        """update_module_light

        Updates the CrawlerLight parameters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the CrawlerLight.
            texts (tuple[str, str, str]): the texts to display in the CrawlerLight. Defaults to ("NOP", "NOP", "NOP").
            level (int): the level (aka. colour) of the CrawlerLight. Defaults to 0.
            report (dict[str, int]): the crawler report.
            selected (bool): indicates if the button is selected.
            blink_flag (bool): indicates if we are in ablink cycle.
            action (Optional[Callable[[], None]]): method to call whn button is pressd. Defaults to None.
        """
        #  Save parameters.

        self.rect = rect
        self.texts = texts
        self.report: dict[str, int] = report
        self.selected = selected
        self.action: Optional[Callable[[], None]] = action

        #  Calculate rects.

        #  Light rect.

        self.light_rect: tuple[int, int, int, int] = (
            self.rect[0],
            self.rect[1],
            self.rect[2] - 108,
            self.rect[3],
        )

        #  Warning rects.

        self.warning_rect1: tuple[int, int, int, int] = (
            self.rect[0] + self.rect[2] - 106,
            self.rect[1],
            40,
            int(self.rect[3] / 3),
        )
        self.warning_rect2: tuple[int, int, int, int] = (
            self.rect[0] + self.rect[2] - 64,
            self.rect[1],
            40,
            int(self.rect[3] / 3),
        )

        self.warning_rect3: tuple[int, int, int, int] = (
            self.rect[0] + self.rect[2] - 106,
            self.rect[1] + int(self.rect[3] / 3) + 1,
            40,
            int(self.rect[3] / 3),
        )
        self.warning_rect4: tuple[int, int, int, int] = (
            self.rect[0] + self.rect[2] - 64,
            self.rect[1] + int(self.rect[3] / 3) + 1,
            40,
            int(self.rect[3] / 3),
        )

        self.warning_rect5: tuple[int, int, int, int] = (
            self.rect[0] + self.rect[2] - 106,
            self.rect[1] + (int(self.rect[3] / 3) * 2) + 2,
            40,
            int(self.rect[3] / 3),
        )
        self.warning_rect6: tuple[int, int, int, int] = (
            self.rect[0] + self.rect[2] - 64,
            self.rect[1] + (int(self.rect[3] / 3) * 2) + 2,
            40,
            int(self.rect[3] / 3),
        )

        #  Button rect.

        self.button_rect: tuple[int, int, int, int] = (
            self.rect[0] + self.rect[2] - 22,
            self.rect[1],
            22,
            self.rect[3],
        )

        #  Get the light colour. The danger colour will be shown during the blink cycle
        #  if the location is occupied and the health is down to zero.
        #  Otherwsie select a colour based on the health of the module.

        # if (
        #     ((percent == 0) or status != "ONLINE")
        #     and (occupied is True)
        #     and blink_flag is False
        # ):
        #     self.light_colour: tuple[int, int, int] = layout_config.danger_colour
        # else:

        _level: int = max(
            int(report["cells"]),
            int(report["oxygen"]),
            int(report["terrain"]),
            int(report["heat"]),
        )
        self.light_colour = get_light_colour(
            _level,
            blink_flag,
        )
        self.warning1_colour: tuple[int, int, int] = get_light_colour(
            int(report["cells"]),
            blink_flag,
        )
        self.warning2_colour: tuple[int, int, int] = get_light_colour(
            int(report["oxygen"]),
            blink_flag,
        )
        self.warning3_colour: tuple[int, int, int] = get_light_colour(
            int(report["terrain"]),
            blink_flag,
        )
        self.warning4_colour: tuple[int, int, int] = get_light_colour(
            int(report["heat"]),
            blink_flag,
        )
        self.warning5_colour: tuple[int, int, int] = get_light_colour(
            0,
            blink_flag,
        )
        self.warning6_colour: tuple[int, int, int] = get_light_colour(
            0,
            blink_flag,
        )

        #  Update Base superclass.

        super().update_base(
            self.light_rect,
            self.light_colour,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the CrawlerLight class.

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

        #  Draw warnings lights.

        _width: int = 1 if int(self.report["cells"]) == 0 else 0
        pygame.draw.rect(display, self.warning1_colour, self.warning_rect1, _width)
        _width: int = 1 if int(self.report["oxygen"]) == 0 else 0
        pygame.draw.rect(display, self.warning2_colour, self.warning_rect2, _width)
        _width: int = 1 if int(self.report["terrain"]) == 0 else 0
        pygame.draw.rect(display, self.warning3_colour, self.warning_rect3, _width)
        _width: int = 1 if int(self.report["heat"]) == 0 else 0
        pygame.draw.rect(display, self.warning4_colour, self.warning_rect4, _width)
        pygame.draw.rect(
            display,
            self.warning5_colour,
            self.warning_rect5,
            1,
        )
        pygame.draw.rect(
            display,
            self.warning6_colour,
            self.warning_rect6,
            1,
            border_bottom_right_radius=self.bot_right_corner_radius,
        )

        #  Darw the button area.

        if self.hover_flag is False:
            _width: int = 1
        else:
            _width = 0

        if self.selected is True:
            _width = 0

        pygame.draw.rect(
            display,
            self.light_colour,
            self.button_rect,
            _width,
            border_bottom_right_radius=self.bot_right_corner_radius,
        )
