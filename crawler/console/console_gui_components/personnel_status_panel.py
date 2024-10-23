#  The PersonnelStatusPanel class provides a panel displaying the status of all the crawler personnel.


import pygame

import crawler.constants as c
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.calculate_panel_current_pos import (
    calculate_current_pos,
)
from crawler.console.console_tools.calculate_panel_end_pos import calculate_end_pos
from crawler.console.console_tools.calculate_panel_start_pos import calculate_start_pos
from crawler.console.console_tools.get_light_colour import get_light_colour
from crawler.console.console_tools.show_text import show_text


class PersonnelStatusPanel(Base):
    """PersonnelStatusPanel

    The PersonnelStatusPanel class provides a panel displaying the status of all the crawler personnel.

    Args:
        Base: The PersonnelStatusPanel class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the PersonnelStatusPanel class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise the PersonnelStatusPanel variables.

        self.x_current_pos: int = c.PANEL_POS_UNSET
        self.y_current_pos: int = c.PANEL_POS_UNSET
        self.showing: bool = False

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        if event.type == pygame.KEYDOWN:
            _keys = pygame.key.get_pressed()

            char_keys_pressed: bool = any(_keys[pygame.K_a + i] for i in range(26))

            if (
                _keys[pygame.K_UP]
                or _keys[pygame.K_DOWN]
                or _keys[pygame.K_LEFT]
                or _keys[pygame.K_RIGHT]
            ):
                if (
                    _keys[pygame.K_RALT]
                    or _keys[pygame.K_LALT]
                    or _keys[pygame.K_RCTRL]
                    or _keys[pygame.K_LCTRL]
                ):
                    layout_config.buzz_sound.play()
                else:
                    self.play_key_sound()
            elif (
                _keys[pygame.K_LCTRL] or _keys[pygame.K_RCTRL]
            ) and not char_keys_pressed:
                self.play_key_sound()
            elif (_keys[pygame.K_LCTRL] or _keys[pygame.K_RCTRL]) and _keys[pygame.K_c]:
                self.play_key_sound()
            else:
                layout_config.buzz_sound.play()

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
        personnel_status: dict[str, tuple[str, int, int]],
        appear: str = "top",
        blink_flag: bool = False,
    ) -> None:
        """updupdate_lightate

        Updates the PersonnelStatusPanel parameters.

        Args:
            dt (float): delta time.
            rect (tuple[int, int, int, int]): the position and size of the PersonnelStatusPanel.
            personnel_status (disct[str, str]): the status of all the personnel.
            appear (str): set where the PersonnelStatusPanel appears from. Deafults to "top".
            blink_flag (bool): indicates if we are in a blinkstate.
        """

        #  Save PersonnelStatusPanel parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.personnel_status: dict[str, tuple[str, int, int]] = personnel_status
        self.blink_flag: bool = blink_flag

        #  Calculate the position of the panel as it moves.

        _x_start_pos: int = 0
        _y_start_pos: int = 0
        _x_end_pos: int = 0
        _y_end_pos: int = 0

        _x_start_pos, _y_start_pos = calculate_start_pos(rect, appear)

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

        Renders the PersonnelStatusPanel class.

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

        #  Draw title.

        show_text(
            subsurface,
            "Personnel Status Report",
            self.base_to_display_rect((25, 8, 80, 30)),
            layout_config.font,
            colour=c.BLACK,
            centered=False,
        )

        #  Draw personnel report.

        self.draw_personnel_section(subsurface)

    def draw_personnel_section(self, subsurface: pygame.Surface) -> None:

        #  Draw outline rectanlge.

        pygame.draw.rect(
            subsurface,
            layout_config.colour,
            self.base_to_display_rect((4, 34, self.rect[2] - 8, self.rect[3] - 68)),
            1,
        )

        #  Draw ten personnel lines.

        _y_pos: int = 38
        self.show_report_line(
            subsurface,
            "Personnel 1:",
            self.personnel_status["Personnel 1"],
            _y_pos,
            self.blink_flag,
        )

        _y_pos += 32
        self.show_report_line(
            subsurface,
            "Personnel 2:",
            self.personnel_status["Personnel 2"],
            _y_pos,
            self.blink_flag,
        )

        _y_pos += 32
        self.show_report_line(
            subsurface,
            "Personnel 3:",
            self.personnel_status["Personnel 3"],
            _y_pos,
            self.blink_flag,
        )

        _y_pos += 32
        self.show_report_line(
            subsurface,
            "Personnel 4:",
            self.personnel_status["Personnel 4"],
            _y_pos,
            self.blink_flag,
        )

        _y_pos += 32
        self.show_report_line(
            subsurface,
            "Personnel 5:",
            self.personnel_status["Personnel 5"],
            _y_pos,
            self.blink_flag,
        )

        _y_pos += 32
        self.show_report_line(
            subsurface,
            "Personnel 6:",
            self.personnel_status["Personnel 6"],
            _y_pos,
            self.blink_flag,
        )

        _y_pos += 32
        self.show_report_line(
            subsurface,
            "Personnel 7:",
            self.personnel_status["Personnel 7"],
            _y_pos,
            self.blink_flag,
        )

        _y_pos += 32
        self.show_report_line(
            subsurface,
            "Personnel 8:",
            self.personnel_status["Personnel 8"],
            _y_pos,
            self.blink_flag,
        )

        _y_pos += 32
        self.show_report_line(
            subsurface,
            "Personnel 9:",
            self.personnel_status["Personnel 9"],
            _y_pos,
            self.blink_flag,
        )

        _y_pos += 32
        self.show_report_line(
            subsurface,
            "Personnel 10:",
            self.personnel_status["Personnel 10"],
            _y_pos,
            self.blink_flag,
        )

        #  Count the number of occupied personnel locations.

        _pesonnel_count: int = 0
        if self.personnel_status["Personnel 1"][0] != "Unused":
            _pesonnel_count += 1
        if self.personnel_status["Personnel 2"][0] != "Unused":
            _pesonnel_count += 1
        if self.personnel_status["Personnel 3"][0] != "Unused":
            _pesonnel_count += 1
        if self.personnel_status["Personnel 4"][0] != "Unused":
            _pesonnel_count += 1
        if self.personnel_status["Personnel 5"][0] != "Unused":
            _pesonnel_count += 1
        if self.personnel_status["Personnel 6"][0] != "Unused":
            _pesonnel_count += 1
        if self.personnel_status["Personnel 7"][0] != "Unused":
            _pesonnel_count += 1
        if self.personnel_status["Personnel 8"][0] != "Unused":
            _pesonnel_count += 1
        if self.personnel_status["Personnel 9"][0] != "Unused":
            _pesonnel_count += 1
        if self.personnel_status["Personnel 10"][0] != "Unused":
            _pesonnel_count += 1

        #  Draw footer

        pygame.draw.rect(
            subsurface,
            layout_config.colour,
            self.base_to_display_rect((0, self.rect[3] - 30, self.rect[2], 30)),
            border_bottom_left_radius=layout_config.corner_radius,
            border_bottom_right_radius=layout_config.corner_radius,
        )

        show_text(
            subsurface,
            f"Personnel[{_pesonnel_count}]",
            self.base_to_display_rect((0, self.rect[3] - 30, self.rect[2], 30)),
            layout_config.font,
            colour=c.BLACK,
            centered=True,
        )

    def show_report_line(
        self,
        surface: pygame.Surface,
        module: str,
        message: tuple[str, int, int],
        y_offset: int,
        blink_flag: bool,
    ) -> None:

        #  Get light colour.

        _normal_colour: tuple[int, int, int] = get_light_colour(100, True)

        #  If offline the colour will be the danger colour.

        if "offline" in message[0]:
            _colour: tuple[int, int, int] = get_light_colour(3, blink_flag)
        else:
            _colour = get_light_colour(message[2], blink_flag)

        #  Draw status entry.

        show_text(
            surface,
            module,
            self.base_to_display_rect((10, y_offset + 7, 80, 30)),
            layout_config.font,
            colour=_normal_colour,
            centered=False,
        )
        pygame.draw.rect(
            surface,
            _colour,
            self.base_to_display_rect((130, y_offset, 700, 30)),
            1,
        )
        show_text(
            surface,
            message[0],
            self.base_to_display_rect((135, y_offset + 7, 800, 30)),
            layout_config.font,
            colour=_colour,
            centered=False,
        )
        pygame.draw.rect(
            surface,
            _colour,
            self.base_to_display_rect((832, y_offset, 60, 30)),
            1,
        )
        show_text(
            surface,
            f"{str(message[1])}%",
            self.base_to_display_rect((832, y_offset, 60, 30)),
            layout_config.font,
            colour=_colour,
            centered=True,
        )

    def play_key_sound(self) -> None:
        if layout_config.key_sound_flag is True:
            layout_config.key_sound.play()
