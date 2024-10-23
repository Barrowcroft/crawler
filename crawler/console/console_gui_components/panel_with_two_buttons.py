#  The PanelWithTwoButtons class provides a panel with two buttons
#  that will slide into view from the edge of the map view.

from typing import Callable

import pygame

from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.button import Button
from crawler.console.console_tools.calculate_panel_current_pos import (
    calculate_current_pos,
)
from crawler.console.console_tools.calculate_panel_end_pos import calculate_end_pos
from crawler.console.console_tools.calculate_panel_start_pos import calculate_start_pos
from crawler.console.console_tools.show_text import show_text

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 30
PANEL_SPEED = 800
POS_UNSET = -10000
BLACK = (1, 1, 1)


class PanelWithTwoButtons(Base):
    """PanelWithTwoButtons

    The PanelWithTwoButtons class provides a panel that will slide into view from the edge of the map view.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The PanelWithTwoButtons class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the PanelWithTwoButtons class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise the PanelWithTwoButtons variables.

        self.x_current_pos: int = POS_UNSET
        self.y_current_pos: int = POS_UNSET
        self.showing: bool = False

        #  Create buttons.

        self.button1: Button = Button()
        self.button2: Button = Button()

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        ...

        if event.type == pygame.KEYDOWN:
            if event.key == getattr(pygame, f"K_{self.key[0]}"):
                self.play_key_sound()
                self.actions[0]()
            elif event.key == getattr(pygame, f"K_{self.key[1]}"):
                self.play_key_sound()
                self.actions[1]()
            elif event.key == pygame.K_ESCAPE:
                self.showing = False
            elif event.key != pygame.K_ESCAPE:
                layout_config.buzz_sound.play()

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
            self.button2.checkClick(
                event, layout_config.map_position[0], layout_config.map_position[1] + 30
            )

        if event.type == pygame.MOUSEMOTION:
            self.button1.checkHover(
                event, layout_config.map_position[0], layout_config.map_position[1] + 30
            )
            self.button2.checkHover(
                event, layout_config.map_position[0], layout_config.map_position[1] + 30
            )

    def update_panel(
        self,
        dt: float,
        rect: tuple[int, int, int, int],
        actions: tuple[Callable[[], None], Callable[[], None]],
        appear: str = "top",
        text: str = "",
        labels: tuple[str, str] = ("", ""),
        keys: tuple[str, str] = ("", ""),
    ) -> None:
        """update_panel

        Updates the PanelWithTwoButtons parameters.

        Args:
            dt (float): delta time.
            rect (tuple[int, int, int, int]): the position and size of the PanelWithTwoButtons.
            actions (tuple[Callable[[], None], Callable[[], None]]): methods to call when the buttons are clicked.
            appear (str): set where the PanelWithTwoButtons appears from. Deafults to "top".
            text (str): the text to display in the PanelWithTwoButtons. Defaults to "".
            labels (tuple[str, str]): the labels for the PanelWithTwoButtons buttons. Defaults to ("","").
            keys (tuple[str, str]): the shortcut keys for the PanelWithTwoButtons buttons. Defaults to ("","").
        """
        #  Save parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.actions: tuple[Callable[[], None], Callable[[], None]] = actions
        self.text: str = text
        self.key: tuple[str, str] = keys

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

        #  Update Buttons.

        self.button1.update_button(
            self.base_to_display_rect(
                (10, self.rect[3] - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT)
            ),
            actions[0],
            labels[0],
            False,
        )

        self.button2.update_button(
            self.base_to_display_rect(
                (
                    self.rect[2] - BUTTON_WIDTH - 10,
                    self.rect[3] - BUTTON_HEIGHT - 10,
                    BUTTON_WIDTH,
                    BUTTON_HEIGHT,
                )
            ),
            actions[1],
            labels[1],
            False,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the PanelWithTwoButtons class.

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

        #  Render Buttons

        self.button1.render(subsurface)
        self.button2.render(subsurface)

    def play_key_sound(self) -> None:
        if layout_config.key_sound_flag is True:
            layout_config.key_sound.play()
