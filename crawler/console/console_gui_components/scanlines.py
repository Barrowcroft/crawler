#  The Scanlines class draws a series of scan line on them map area.

import random

import pygame

from crawler.config import layout_config

CRT_ALPHA = 25


class Scanlines:
    """Scanlines

    The Scanlines class draws a series of scan line on them map area.
    Imports the layout_config to obtain layout information.
    """

    def __init__(self) -> None:
        """__init__

        Initialise the Scanlines class.
        """
        self.scanlines_timer: float = 0

    def update(
        self,
        dt: float,
        rect: tuple[int, int, int, int],
    ) -> None:
        """udate

        Updates the Scanlines.

        Args:
            dt (float): delta time.
            rect (tuple[int, int, int, int]): the position and size of the Scanlines rectangle.
        """

        #  Save Scanlines parameters.

        self.rect = rect
        self.scanlines_timer -= dt
        self.scanline: int = 0

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the console crt effect.

        Args:
            display (pygame.Surface): display to render on to.
        """
        #  Draw crt effect.

        self.draw_scanlines(display, self.rect)

        if self.scanlines_timer < 0:

            self.scanline = self.draw_extra_scanlines(display, self.rect, self.scanline)

            if self.scanline == 0:
                self.scanlines_timer = random.randint(5, 10)

    def draw_scanlines(
        self, display: pygame.Surface, rect: tuple[int, int, int, int]
    ) -> None:

        #  Creat new surface and set alpha.

        _crt = pygame.Surface((rect[2], rect[3]))
        _crt.set_alpha(CRT_ALPHA)

        #  Draw crt scan lines.

        _y_start: int = 0

        for _y in range(_y_start, rect[1] + rect[3], 3):
            if _y % 5 == 0:
                pygame.draw.line(_crt, layout_config.colour, (0, _y), (rect[2], _y), 3)
            else:
                pygame.draw.line(
                    _crt,
                    layout_config.colour,
                    (0, _y),
                    (rect[2], _y),
                )

        for _y in range(_y_start, rect[1] + rect[3], random.randint(5, 20)):
            if _y % 5 == 0:
                pygame.draw.line(_crt, layout_config.colour, (0, _y), (rect[2], _y), 5)
            else:
                pygame.draw.line(_crt, layout_config.colour, (0, _y), (rect[2], _y), 3)

        #  Blit crt.

        display.blit(_crt, (rect[0], rect[1]))

    def draw_extra_scanlines(
        self, display: pygame.Surface, rect: tuple[int, int, int, int], next: int
    ) -> int:

        #  Creat new surface and set alpha.

        _crt = pygame.Surface((rect[2], rect[3]))
        _crt.set_alpha(CRT_ALPHA - 5)

        #  Draw crt scan lines.

        pygame.draw.line(_crt, layout_config.colour, (0, next), (rect[2], next), 5)

        #  Blit crt.

        display.blit(_crt, (rect[0], rect[1]))

        #  Return next line.

        if next == rect[3]:
            return 0
        else:
            return next + 1
