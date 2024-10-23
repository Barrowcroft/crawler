#  The MiniMap class.

from typing import Callable

import pygame

import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.scanlines import Scanlines
from crawler.console.console_tools.draw_minimap_cursor import draw_minimap_cursor
from crawler.console.console_tools.draw_minimap_scan import draw_minimap_scan
from crawler.console.console_tools.show_text import show_text

BLACK = (0, 0, 0)


class MiniMap(Base):
    """MiniMap

    The MiniMap class.

    Args:
        Base: The MiniMap class subclases the Base class.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(
        self,
    ) -> None:
        """__init__

        Initialise the MiniMap.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise the CRT sanlines.

        self.scanlines: Scanlines = Scanlines()

        #  Initialise the scan variables.

        self.scan_targets: list[tuple[int, int]] = []
        self.scan_timer: float = 0
        self.scan_y_offset: int = 0
        self.scan: bool = False

    def update_minimap(
        self,
        dt: float,
        mini_map: pygame.surface.Surface,
        rect: tuple[int, int, int, int],
        crawler_position: tuple[int, int] = (0, 0),
        signal_flag: bool = False,
    ) -> None:
        """update_minimap

        Updates the MiniMap.
        Args:
            dt (float): delta time.
            mini_map (pygame.surface.Surface): the mini map image.
            rect (tuple[int, int, int, int]): the position and size of the MiniMap..
            crawler_posiion (tuple[int, int]): position of the crawler.
            signal_flag (bool): indications if there is a signal. Defaults to True.
        """
        #  Save MiniMap parameters.

        self.mnini_map: pygame.surface.Surface = mini_map
        self.rect: tuple[int, int, int, int] = rect
        self.crawler_position: tuple[int, int] = crawler_position
        self.signal_flag: bool = signal_flag

        #  Create / update colour conversion.

        if self.colour != layout_config.colour:
            self.colour_view = pygame.Surface(
                (self.rect[2] - 2, self.rect[3] - 2), pygame.SRCALPHA
            )
            self.colour_view.fill(layout_config.colour)
            self.colour = layout_config.colour

        #  Update Base superclass.

        super().update_base(rect, colour=layout_config.colour)

        #  Update CRT Scanlines.

        # if layout_config.scanlines_flag is True:
        #     self.scanlines.update(dt, rect)

        #  Update scan timers.

        self.scan_timer += dt
        if self.scan_timer > 0.02:  #  Advance scan line by one pixel every 0.02 dt
            self.scan_timer = 0
            self.scan_y_offset += 1

    def render(self, display: pygame.Surface) -> None:
        """render

        Render the MiniMap
        Args:
            display (pygame.event.Event): display on which to render.
        """

        #  Render the Base superclass.

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
            #  Render the mini map

            display.blit(self.mnini_map, (self.rect[0] + 1, self.rect[1] + 1))

            #  Add colour conversion.

            display.blit(
                self.colour_view,
                (self.rect[0] + 1, self.rect[1] + 1),
                special_flags=pygame.BLEND_MULT,
            )

            #  Render CRT scanlines.

            # if layout_config.scanlines_flag is True:
            #     self.scanlines.render(display)

            #  If scan is true draw scan line.

            if self.scan is True:
                self.scan = draw_minimap_scan(
                    display,
                    self.rect,
                    self.scan_targets,
                    self.scan_y_offset,
                )

                if self.scan is False:
                    self.callback()

            #  Draw cursor.

            draw_minimap_cursor(display, self.rect, self.crawler_position)

    #  Functions that may be called from functions in the parent class.

    def start_scan(
        self, scan_targets: list[tuple[int, int]], callback: Callable[[], None]
    ) -> None:
        self.scan_targets = scan_targets
        self.scan = True
        self.scan_timer = 0
        self.scan_y_offset = 0
        self.callback: Callable[[], None] = callback

    def abort_scan(self) -> None:
        self.scan = False
        self.scan_timer = 0
