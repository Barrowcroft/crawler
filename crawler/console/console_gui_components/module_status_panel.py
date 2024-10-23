#  The ModuleStatusPanel class provides a panel displaying the status of all the crawler modules.


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


class ModuleStatusPanel(Base):
    """ModuleStatusPanel

    The ModuleStatusPanel class provides a panel displaying the status of all the crawler modules.

    Args:
        Base: The ModuleStatusPanel class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the ModuleStatusPanel class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise the ModuleStatusPanel variables.

        self.x_current_pos: int = c.PANEL_POS_UNSET
        self.y_current_pos: int = c.PANEL_POS_UNSET
        self.y_pos: int = 0
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
        module_status: dict[str, tuple[str, int, int]],
        appear: str = "top",
        blink_flag: bool = False,
    ) -> None:
        """updupdate_lightate

        Updates the ModuleStatusPanel parameters.

        Args:
            dt (float): delta time.
            rect (tuple[int, int, int, int]): the position and size of the ModuleStatusPanel.
            module_status (disct[str, str]): the status of all the modules.
            appear (str): set where the ModuleStatusPanel appears from. Deafults to "top".
            blink_flag (bool): indicates if we are in a blinkstate.
        """

        #  Save ModuleStatusPanel parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.module_status: dict[str, tuple[str, int, int]] = module_status
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

        Renders the ModuleStatusPanel class.

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
            "Module Status Report",
            self.base_to_display_rect((25, 8, 80, 30)),
            layout_config.font,
            colour=c.BLACK,
            centered=False,
        )

        #  Draw system modules section.

        self.draw_system_modules_section(subsurface)
        self.draw_optional_modules_section(subsurface)

        #  Draw footer.

        self.draw_footer(subsurface)

    def draw_system_modules_section(self, subsurface: pygame.Surface) -> None:

        pygame.draw.rect(
            subsurface,
            layout_config.colour,
            self.base_to_display_rect((4, 34, self.rect[2] - 8, 198)),
            1,
        )

        self.y_pos: int = 38
        self.show_report_line(
            subsurface,
            "Oxygen:",
            self.module_status["Oxygen Supply Module"],
            self.y_pos,
            self.blink_flag,
        )
        self.y_pos += 32
        self.show_report_line(
            subsurface,
            "Power Cells:",
            self.module_status["Power Cells Module"],
            self.y_pos,
            self.blink_flag,
        )
        self.y_pos += 32
        self.show_report_line(
            subsurface,
            "Engine:",
            self.module_status["Engine Module"],
            self.y_pos,
            self.blink_flag,
        )
        self.y_pos += 32
        self.show_report_line(
            subsurface,
            "Cooler:",
            self.module_status["Cooler Module"],
            self.y_pos,
            self.blink_flag,
        )
        self.y_pos += 32
        self.show_report_line(
            subsurface,
            "Life-Support:",
            self.module_status["Life-Support Module"],
            self.y_pos,
            self.blink_flag,
        )
        self.y_pos += 32
        self.show_report_line(
            subsurface, "Hold:", self.module_status["Hold"], self.y_pos, self.blink_flag
        )

    def draw_optional_modules_section(self, subsurface: pygame.Surface) -> None:

        pygame.draw.rect(
            subsurface,
            layout_config.colour,
            self.base_to_display_rect((4, 234, self.rect[2] - 8, 198)),
            1,
        )

        self.y_pos += 40
        self.show_report_line(
            subsurface,
            "Module 1:",
            self.module_status["Module 1"],
            self.y_pos,
            self.blink_flag,
        )

        self.y_pos += 32
        self.show_report_line(
            subsurface,
            "Module 2:",
            self.module_status["Module 2"],
            self.y_pos,
            self.blink_flag,
        )

        self.y_pos += 32
        self.show_report_line(
            subsurface,
            "Module 3:",
            self.module_status["Module 3"],
            self.y_pos,
            self.blink_flag,
        )

        self.y_pos += 32
        self.show_report_line(
            subsurface,
            "Module 4:",
            self.module_status["Module 4"],
            self.y_pos,
            self.blink_flag,
        )

        self.y_pos += 32
        self.show_report_line(
            subsurface,
            "Module 5:",
            self.module_status["Module 5"],
            self.y_pos,
            self.blink_flag,
        )

        self.y_pos += 32
        self.show_report_line(
            subsurface,
            "Module 6:",
            self.module_status["Module 6"],
            self.y_pos,
            self.blink_flag,
        )

    def draw_footer(self, subsurface: pygame.Surface) -> None:

        #  Count modules.

        _module_count: int = 0
        if self.module_status["Module 1"][0] != "Unused":
            _module_count += 1
        if self.module_status["Module 2"][0] != "Unused":
            _module_count += 1
        if self.module_status["Module 3"][0] != "Unused":
            _module_count += 1
        if self.module_status["Module 4"][0] != "Unused":
            _module_count += 1
        if self.module_status["Module 5"][0] != "Unused":
            _module_count += 1
        if self.module_status["Module 6"][0] != "Unused":
            _module_count += 1

        #  Draw footer and add text.

        pygame.draw.rect(
            subsurface,
            layout_config.colour,
            self.base_to_display_rect((0, 436, self.rect[2], 30)),
            border_bottom_left_radius=layout_config.corner_radius,
            border_bottom_right_radius=layout_config.corner_radius,
        )

        show_text(
            subsurface,
            f"System Modules [6]  Optional Modules [{_module_count}]",
            self.base_to_display_rect((0, 436, self.rect[2], 30)),
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

        #  Get light colours.

        _normal_colour: tuple[int, int, int] = get_light_colour(1, True)

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
            self.base_to_display_rect((135, y_offset + 7, 700, 30)),
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
