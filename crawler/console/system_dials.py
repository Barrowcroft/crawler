#  The system_dials file describes the SystemDials class.

import pygame

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.dial import Dial
from crawler.console.console_tools.show_text import show_text


class SystemDials(Base):
    """SystemDials

    The system_dials file describes the SystemDials class.

    Args:
        Base: The SystemDials sublasses the Base class.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(self) -> None:
        """__init__

        Initialises the SystemDials.
        """
        super().__init__()

        #  Initialise the dials.

        self.dial_texts: list[str] = [
            "CELLS",
            "OXYGEN",
            "REVS",
            "SPEED",
            "HEAT",
        ]

        self.dial_levels: list[int] = []
        self.dial_percent: list[int] = []
        self.dial_layouts: list[tuple[int, int, int, int]] = c.DIAL_LAYOUTS

        #  Initialise the blink_flag and beep variables.

        self.blink_flag: bool = False
        self.request_beep: bool = False

        #  Create dials.

        self.dials = [Dial() for _ in range(5)]

    def update_system_dials(
        self,
        dt: float,
        rect: tuple[int, int, int, int],
        levels: list[int] = [],
        percent: list[int] = [],
        blink_flag: bool = False,
        signal_flag: bool = False,
    ) -> None:
        """update_system_dials

        Updates the SystemDials.

        Args:
            dt (float): delta time.
            rect (tuple[int, int, int, int]): the position and size of the SystemDials.
            levels (list[int]): the light levels (aka. colour) of the SystemDials. Defaults to an empty list.
            percent (list[int]): the percent of the SystemDialss. Defaults to an empty list.
            blink_flag (bool): indicates if the lights are in blink_flag cycle. Defauls to False.
            signal_flag (bool): indications if there is a signal. Defaults to True.
        """
        #  Save parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.dial_levels: list[int] = levels
        self.dial_percent: list[int] = percent
        self.blink_flag: bool = blink_flag
        self.signal_flag: bool = signal_flag

        #  Update superclass.

        super().update_base(rect, colour=layout_config.colour)

        #  Update dials.

        for _index, _dial in enumerate(self.dials):

            _dial.update_dial(
                self.base_to_display_rect(self.dial_layouts[_index]),
                text=self.dial_texts[_index],
                level=self.dial_levels[_index],
                percent=self.dial_percent[_index],
                blink_flag=blink_flag,
            )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the console dials.

        Args:
            display (pygame.Surface): display to render on to.
        """

        super().render(display)

        if self.signal_flag is False:
            show_text(
                display,
                "No signal",
                self.rect,
                layout_config.font,
                self.colour,
            )
        else:

            #  Draw the dials

            for _dial in self.dials:
                _dial.render(display)

        #  If any of the levels are a level 3 then we need to set the beep on.

        self.request_beep = False
        for _level in self.dial_levels:
            if _level == 3:
                self.request_beep = True
                break
