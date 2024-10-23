#  The PanelWithOneButton class provides a panel
#  that will slide into view from the edge of the map view.


import pygame

import crawler.constants as c
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.calculate_panel_current_pos import (
    calculate_current_pos,
)
from crawler.console.console_tools.calculate_panel_end_pos import calculate_end_pos
from crawler.console.console_tools.calculate_panel_start_pos import calculate_start_pos
from crawler.console.console_tools.show_text import show_text


class PanelWithNoButton(Base):
    """PanelWithNoButton

    The PanelWithNoButton class provides a panel that will slide into view from the edge of the map view.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The PanelWithNoButton class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the PanelWithNoButton class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise the PanelWithNoButton variables.

        self.x_current_pos: int = c.PANEL_POS_UNSET
        self.y_current_pos: int = c.PANEL_POS_UNSET
        self.showing: bool = False

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        ...

    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        ...

    def update_panel(
        self,
        dt: float,
        rect: tuple[int, int, int, int],
        appear: str = "top",
        text: str = "",
    ) -> None:
        """update_panel

        Updates the PanelWithNoButton parameters.

        Args:
            dt (float): delta time.
            rect (tuple[int, int, int, int]): the position and size of the PanelWithNoButton.
            appear (str): set where the PanelWithNoButton appears from. Deafults to "top".
            text (str): the text to display in the PanelWithNoButton. Defaults to "".
        """
        #  Save parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.text: str = text

        #  Calculate the position of the panel as it moves.

        _x_start_pos: int = 0
        _y_start_pos: int = 0

        if _x_start_pos == 0:
            _x_start_pos, _y_start_pos = calculate_start_pos(rect, appear)

        _x_end_pos: int = 0
        _y_end_pos: int = 0

        if _x_end_pos == 0:
            _x_end_pos, _y_end_pos = calculate_end_pos(rect, appear)

        self.x_current_pos, self.y_current_pos = calculate_current_pos(
            dt,
            appear,
            _x_start_pos,
            _y_start_pos,
            _x_end_pos,
            _y_end_pos,
            self.x_current_pos,
            self.y_current_pos,
            self.showing,
        )

        #  Update Base superclass.

        super().update_base(
            (self.x_current_pos, self.y_current_pos, rect[2], rect[3]),
            colour=layout_config.colour,
            corner_radius=layout_config.corner_radius,
            bar=True,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the PanelWithNoButton class.

        Args:
            display (pygame.Surface): display on which to render.
        """
        #  Render the superclass on a new surface corresponding to the map pane.

        subsurface = display.subsurface(
            (
                layout_config.map_position[0] + 2,
                layout_config.map_position[1] + 32,
                layout_config.map_position[2] - 4,
                layout_config.map_position[3] - 64,
            )
        )
        super().render(subsurface)

        #  Draw the text.

        show_text(
            subsurface,
            self.text,
            self.rect,
            layout_config.font,
            colour=layout_config.colour,
        )
