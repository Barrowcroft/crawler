#  The Menu class.

from typing import Callable

import pygame

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.button import Button
from crawler.console.console_tools.show_text import show_text


class Menu(Base):
    """Menu

    The Menu class.

    Args:
        Base: The Menu subclasses the Base class.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(
        self,
    ) -> None:

        #  Initialise the Base superclass.

        super().__init__()

        #  Create menu buttons.

        self.menu: list[
            tuple[
                str,
                Callable[
                    [],
                    None,
                ],
                bool,
            ]
        ] = []
        self.menu_buttons = [Button() for _ in range(10)]

    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.
        Coordinates the handling of events by other classes.

        Args:
            event (pygame.event.Event): event to handle.
        """

        #  If there are no menu options then return immed.

        if self.menu == []:
            return

        #  Process event in each button.

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.menu_buttons:
                button.checkClick(event)

        if event.type == pygame.MOUSEMOTION:
            for button in self.menu_buttons:
                button.checkHover(event)

    def update_menu(
        self,
        rect: tuple[int, int, int, int],
        signal_flag: bool = False,
        menu: list[tuple[str, Callable[[], None], bool]] = [],
    ) -> None:
        """update_menu

        Update the Menu.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the Menu.
            signal_flag (bool): indicates if there is a signal. Defauls to True.
            menu (list[tuple[str, Callable[[],None]]]): menu items to display in  Menu.
        """
        #  Save Menu parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.signal_flag: bool = signal_flag
        self.menu: list[tuple[str, Callable[[], None], bool]] = menu

        #  Update the Base superclass.

        super().update_base(
            rect,
            colour=layout_config.colour,
            corner_radius=layout_config.corner_radius,
            bar=True,
        )

        #  Update Buttons. The dimished colour will be used for disabled buttons.

        _x_pos: int = 4
        _y_pos: int = 0

        _colour = (
            int(self.colour[0] / 1.5),
            int(self.colour[1] / 1.5),
            int(self.colour[2] / 1.5),
        )

        _diminished_colour = (
            int(self.colour[0] / 4),
            int(self.colour[1] / 4),
            int(self.colour[2] / 4),
        )

        for index, button in enumerate(self.menu_buttons):

            #  Layout menu buttons in two columns.

            _y_pos = index * 38

            if index > 4:
                _x_pos = 4 + int((rect[2] / 2) - 2)
                _y_pos = (index - 5) * 38

            #  Update buttons.

            if index < len(self.menu):

                button.update_button(
                    self.base_to_display_rect(
                        (_x_pos, 34 + _y_pos, int((rect[2] / 2) - 6), 34)
                    ),
                    self.menu[index][1],
                    self.menu[index][0],
                    self.menu[index][2],
                )

    def render(self, display: pygame.Surface) -> None:
        """render

        Args:
            display (pygame.event.Event): display on which to render..
        """

        #  Render the Base superclass.

        super().render(display)

        #  Render the Menu.

        show_text(
            display,
            "SERVICES",
            self.base_to_display_rect((0, 0, self.rect[2], 30)),
            layout_config.font,
            c.BLACK,
        )

        #  Render Menu buttons.

        for button in self.menu_buttons:
            button.render(display)

    def disable_all_but(self, index: int) -> None:
        self.disable_all()
        self.menu[index] = (self.menu[index][0], self.menu[index][1], False)

    def disable_all(self) -> None:
        for index in range(10):
            self.menu[index] = (self.menu[index][0], self.menu[index][1], True)

    def disable(self, index: int) -> None:
        self.menu[index] = (self.menu[index][0], self.menu[index][1], True)

    def enable_all(self) -> None:
        for index in range(10):
            if self.menu[index][0] != "nop":
                self.menu[index] = (self.menu[index][0], self.menu[index][1], False)

    def enable(self, index: int) -> None:
        self.menu[index] = (self.menu[index][0], self.menu[index][1], False)
