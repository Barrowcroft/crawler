#  The  Slider class is a simple slider control.
from typing import Callable

import pygame

import crawler.constants as c
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.show_text import show_text


class Slider(Base):
    """Slider

    The slider.py file provides a display a slider and manage key events on it.

    Args:
        Base: Slider is a subclass of Base.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Initialises the 'Slider'.
        """

        #  Initialse the Base superclass.

        super().__init__()

        #  Initialise the Slider variables.

        self.value: int = 0
        self.dragging: bool = False

    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.

        Args:
            event (pygame.event.Event): event to handle.
        """

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.collision__rect.collidepoint(event.pos):
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:

            self.dragging = False

        if event.type == pygame.MOUSEMOTION:
            if self.dragging is True:
                self.value = (event.pos[0] - (self.rect[0])) / 2
                self.value = min(255, self.value)
                self.value = max(0, self.value)
                self.callback()

    def update_slider(
        self, rect: tuple[int, int, int, int], callback: Callable[[], None], value: int
    ) -> None:
        """update

        Updates the slider

        Args:
            rect (rect: tuple[int, int, int, int]): the rectangle cotnaining the slider.
            callback (Callable[[], None]): the method to call when the mouse move to update the value.
            value (int): the value to display on the slider.
        """

        #  Svae the Slider variables.

        self.value = value
        self.callback: Callable[[], None] = callback

        #  Update the Base superclass.

        super().update_base(rect, background_flag=True)

        #  value is in range 0-255, convert to 0-500

        _show_value: int = self.value * 2
        if _show_value > (c.SLIDER_SIZE[0] - (c.SLIDER_MARGIN * 2)):
            _show_value = c.SLIDER_SIZE[0] - (c.SLIDER_MARGIN * 2)

        #  Update the collision rectangle for click and hover checking.

        self.collision__rect: pygame.rect.Rect = pygame.rect.Rect(
            self.rect[0] + _show_value,
            self.rect[1],
            10,
            25,
        )

        #  Draw the value rectangle.

        self.value_rect: pygame.rect.Rect = pygame.rect.Rect(_show_value, 5, 10, 21)

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the slider.

        Args:
            surface (Surface): the surface to render on to.
        """

        #  Render the superclass.

        super().render(display)

        #  Draw the Slider.

        pygame.draw.line(
            display,
            layout_config.colour,
            (self.rect[0] + 10, self.rect[1] + 15),
            (self.rect[0] + 510, self.rect[1] + 15),
        )
        pygame.draw.line(
            display,
            layout_config.colour,
            (self.rect[0] + 10, self.rect[1] + 5),
            (self.rect[0] + 10, self.rect[1] + 25),
        )
        pygame.draw.line(
            display,
            layout_config.colour,
            (self.rect[0] + 135, self.rect[1] + 5),
            (self.rect[0] + 135, self.rect[1] + 25),
        )
        pygame.draw.line(
            display,
            layout_config.colour,
            (self.rect[0] + 260, self.rect[1] + 5),
            (self.rect[0] + 260, self.rect[1] + 25),
        )
        pygame.draw.line(
            display,
            layout_config.colour,
            (self.rect[0] + 385, self.rect[1] + 5),
            (self.rect[0] + 385, self.rect[1] + 25),
        )
        pygame.draw.line(
            display,
            layout_config.colour,
            (self.rect[0] + 510, self.rect[1] + 5),
            (self.rect[0] + 510, self.rect[1] + 25),
        )

        pygame.draw.rect(
            display,
            layout_config.warning_colour,
            self.base_to_display_rect(
                (
                    self.value_rect[0],
                    self.value_rect[1],
                    self.value_rect[2],
                    self.value_rect[3],
                )
            ),
        )

        #  Add the labels on the Slider.

        show_text(
            display,
            "0",
            self.base_to_display_rect((12, 15, 10, 20)),
            layout_config.small_font_obj,
            layout_config.colour,
            False,
            0,
            1,
        )
        show_text(
            display,
            "255",
            self.base_to_display_rect((485, 15, 10, 20)),
            layout_config.small_font_obj,
            layout_config.colour,
            False,
            0,
            1,
        )
