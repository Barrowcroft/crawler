#  The PanelWithOneButton class provides a panel with one button
#  that will slide into view from the edge of the map view.


from typing import Callable

import pygame

import crawler.constants as c
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.button import Button
from crawler.console.console_tools.calculate_panel_current_pos import (
    calculate_current_pos,
)
from crawler.console.console_tools.calculate_panel_end_pos import calculate_end_pos
from crawler.console.console_tools.calculate_panel_start_pos import calculate_start_pos
from crawler.console.console_tools.show_text import show_text


class PanelWithOneButton(Base):
    """PanelWithOneButton

    The PanelWithOneButton class provides a basic panel that will slide into view from the edge of the map view.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The PanelWithOneButton class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the PanelWithOneButton class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise PanelWithOneButton variables.

        self.x_current_pos: int = c.PANEL_POS_UNSET
        self.y_current_pos: int = c.PANEL_POS_UNSET
        self.showing: bool = False

        #  Create button.

        self.button1: Button = Button()

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        ...

        if event.type == pygame.KEYDOWN:
            if event.key == getattr(pygame, f"K_{self.key}"):
                self.action()

    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.

        Args:
            event (pygame.event.Event): event to handle.
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.button1.checkClick(
                event, layout_config.map_position[0], layout_config.map_position[1] + 30
            )

        if event.type == pygame.MOUSEMOTION:
            self.button1.checkHover(
                event, layout_config.map_position[0], layout_config.map_position[1] + 30
            )

    def update_panel(
        self,
        dt: float,
        rect: tuple[int, int, int, int],
        action: Callable[[], None],
        appear: str = "top",
        text: str = "",
        label: str = "",
        key: str = " ",
    ) -> None:
        """update_panel

        Updates the PanelWithOneButton parameters.

        Args:
            dt (float): delta time.
            rect (tuple[int, int, int, int]): the position and size of the PanelWithOneButton.
            action (Callable[[], None]): method to call when the button is clicked.
            appear (str): set where the PanelWithOneButton appears from. Deafults to "top".
            text (str): the text to display in the PanelWithOneButton. Defaults to "".
            laeb (str): the label to display on the button. Defaults to "".
            key (str): the shortcut key for the PanelWithTwoButtons buttons. Defaults to "".
        """
        #  Save parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.action: Callable[[], None] = action
        self.text: str = text
        self.key: str = key

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

        #  Update Button.

        self.button1.update_button(
            self.base_to_display_rect(
                (
                    10,
                    self.rect[3] - c.PANEL_BUTTON_HEIGHT - 10,
                    c.PANEL_BUTTON_WIDTH,
                    c.PANEL_BUTTON_HEIGHT,
                )
            ),
            action,
            label,
            False,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the class.

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

        #  Render Button.

        self.button1.render(subsurface)
