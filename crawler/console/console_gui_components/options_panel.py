#  The OptionsPanel class describes the program options panel.


import pygame

import crawler.constants as c
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.slider import Slider
from crawler.console.console_gui_components.switch import Switch
from crawler.console.console_tools.calculate_panel_current_pos import (
    calculate_current_pos,
)
from crawler.console.console_tools.show_text import show_text


class OptionsPanel(Base):
    """OptionsPanel

    The OptionsPanel class describes the program options panel.

    Args:
        Base: The OptionsPanel class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the OptionsPanel class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise the OptionsPanel variables.

        self.x_current_pos: int = c.PANEL_POS_UNSET
        self.y_current_pos: int = c.PANEL_POS_UNSET
        self.showing: bool = False

        #  Initialise the switches and sliders.

        self.map_top_left_switch: Switch = Switch()
        self.map_bottom_left_switch: Switch = Switch()
        self.map_top_middle_switch: Switch = Switch()
        self.map_bottom_middle_switch: Switch = Switch()
        self.map_top_right_switch: Switch = Switch()
        self.map_bottom_right_switch: Switch = Switch()

        self.status_left: Switch = Switch()
        self.status_right: Switch = Switch()

        self.terminal_left: Switch = Switch()
        self.terminal_right: Switch = Switch()

        self.minimap_top: Switch = Switch()
        self.minimap_bottom: Switch = Switch()

        self.hold_top: Switch = Switch()
        self.hold_bottom: Switch = Switch()

        self.red_slider: Slider = Slider()
        self.green_slider: Slider = Slider()
        self.blue_slider: Slider = Slider()

        self.curved_corner_toggle: Switch = Switch()
        self.background_toggle: Switch = Switch()
        self.frame_toggle: Switch = Switch()
        self.scan_lines_toggle: Switch = Switch()

        self.alarm_sounds_toggle: Switch = Switch()
        self.scanner_sounds_toggle: Switch = Switch()
        self.button_sounds_toggle: Switch = Switch()
        self.keyboard_sounds_toggle: Switch = Switch()
        self.ambient_sounds_toggle: Switch = Switch()

        self.streamer_mode_toggle: Switch = Switch()

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
            elif (_keys[pygame.K_LCTRL] or _keys[pygame.K_RCTRL]) and _keys[pygame.K_l]:
                self.play_key_sound()
                layout_config.save_current_layout()
            else:
                layout_config.buzz_sound.play()

    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.

        Args:
            event (pygame.event.Event): event to handle.
        """

        self.map_top_left_switch.handleMouseEvent(event)
        self.map_bottom_left_switch.handleMouseEvent(event)
        self.map_top_middle_switch.handleMouseEvent(event)
        self.map_bottom_middle_switch.handleMouseEvent(event)
        self.map_top_right_switch.handleMouseEvent(event)
        self.map_bottom_right_switch.handleMouseEvent(event)
        self.status_left.handleMouseEvent(event)
        self.status_right.handleMouseEvent(event)
        self.terminal_left.handleMouseEvent(event)
        self.terminal_right.handleMouseEvent(event)
        self.minimap_top.handleMouseEvent(event)
        self.minimap_bottom.handleMouseEvent(event)
        self.hold_top.handleMouseEvent(event)
        self.hold_bottom.handleMouseEvent(event)

        self.red_slider.handleMouseEvent(event)
        self.green_slider.handleMouseEvent(event)
        self.blue_slider.handleMouseEvent(event)

        self.curved_corner_toggle.handleMouseEvent(event)
        self.background_toggle.handleMouseEvent(event)
        self.frame_toggle.handleMouseEvent(event)
        self.scan_lines_toggle.handleMouseEvent(event)

        self.alarm_sounds_toggle.handleMouseEvent(event)
        self.scanner_sounds_toggle.handleMouseEvent(event)
        self.button_sounds_toggle.handleMouseEvent(event)
        self.keyboard_sounds_toggle.handleMouseEvent(event)
        self.ambient_sounds_toggle.handleMouseEvent(event)
        self.streamer_mode_toggle.handleMouseEvent(event)

    def update_panel(
        self,
        dt: float,
        rect: tuple[int, int, int, int],
        appear: str = "top",
        text: str = "",
    ) -> None:
        """updupdate_lightate

        Updates the OptionsPanel parameters.

        Args:
            dt (float): delta time.
            rect (tuple[int, int, int, int]): the position and size of the OptionsPanel.
            appear (str): set where the OptionsPanel appears from. Deafults to "top".
            text (str): the text to display in the OptionsPanel. Defaults to "".
        """
        #  Save OptionsPanel parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.text: str = text

        #  Calculate the position of the panel as it moves.

        _x_start_pos: int = 0
        _y_start_pos: int = 0
        _x_end_pos: int = 0
        _y_end_pos: int = 0

        _x_start_pos, _y_start_pos = (
            rect[0],
            -rect[3],
        )

        _x_end_pos, _y_end_pos = rect[0], rect[1]

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

        #  Update switches and sliders.

        self.update_map_position_switches()
        self.update_colour_sliders()
        self.update_misc_switches()
        self.update_sound_switches()
        self.update_streamer_switches()

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the OptionsPanel class.

        Args:
            display (pygame.Surface): display on which to render.
        """
        #  Render the Base superclass.

        super().render(display)

        #  Render text, switches and sliders.

        pygame.draw.rect(
            display,
            layout_config.colour,
            self.base_to_display_rect((4, 34, self.rect[2] - 8, 208)),
            1,
        )

        show_text(
            display,
            "Options",
            self.base_to_display_rect((25, 8, 80, 30)),
            layout_config.font,
            colour=c.BLACK,
            centered=False,
        )

        _y_pos: int = 48
        show_text(
            display,
            "Map position:",
            self.base_to_display_rect((10, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        _y_pos += 64
        show_text(
            display,
            "Status Info position:",
            self.base_to_display_rect((10, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        _y_pos += 34
        show_text(
            display,
            "Terminal position:",
            self.base_to_display_rect((10, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        _y_pos += 34
        show_text(
            display,
            "Minimap position:",
            self.base_to_display_rect((10, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        _y_pos += 34
        show_text(
            display,
            "Hold Info position:",
            self.base_to_display_rect((10, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        self.map_top_left_switch.render(display)
        self.map_bottom_left_switch.render(display)
        self.map_top_middle_switch.render(display)
        self.map_bottom_middle_switch.render(display)
        self.map_top_right_switch.render(display)
        self.map_bottom_right_switch.render(display)

        self.status_left.render(display)
        self.status_right.render(display)

        self.terminal_left.render(display)
        self.terminal_right.render(display)

        self.minimap_top.render(display)
        self.minimap_bottom.render(display)

        self.hold_top.render(display)
        self.hold_bottom.render(display)

        self.curved_corner_toggle.render(display)
        self.background_toggle.render(display)
        self.frame_toggle.render(display)
        self.scan_lines_toggle.render(display)

        self.alarm_sounds_toggle.render(display)
        self.scanner_sounds_toggle.render(display)
        self.button_sounds_toggle.render(display)
        self.keyboard_sounds_toggle.render(display)
        self.ambient_sounds_toggle.render(display)
        self.streamer_mode_toggle.render(display)

        pygame.draw.rect(
            display,
            layout_config.colour,
            self.base_to_display_rect((4, 245, self.rect[2] - 8, 100)),
            1,
        )

        _y_pos += 45
        show_text(
            display,
            "Colour",
            self.base_to_display_rect((10, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        show_text(
            display,
            f"Red:",
            self.base_to_display_rect((120, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )
        show_text(
            display,
            f"{layout_config.colour[0]}",
            self.base_to_display_rect((190, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        self.red_slider.render(display)

        _y_pos += 30
        show_text(
            display,
            f"Green:",
            self.base_to_display_rect((120, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )
        show_text(
            display,
            f"{layout_config.colour[1]}",
            self.base_to_display_rect((190, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        self.green_slider.render(display)

        _y_pos += 30
        show_text(
            display,
            f"Blue:",
            self.base_to_display_rect((120, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )
        show_text(
            display,
            f"{layout_config.colour[2]}",
            self.base_to_display_rect((190, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        self.blue_slider.render(display)

        pygame.draw.rect(
            display,
            layout_config.colour,
            self.base_to_display_rect((4, 348, self.rect[2] - 8, 174)),
            1,
        )

        _y_pos = 362
        show_text(
            display,
            "Show Curved Corners:",
            self.base_to_display_rect((10, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )
        show_text(
            display,
            "Play Alarm Sounds:",
            self.base_to_display_rect((410, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        _y_pos += 34
        show_text(
            display,
            "Show Background:",
            self.base_to_display_rect((10, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )
        show_text(
            display,
            "Play Scanner Sounds:",
            self.base_to_display_rect((410, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        _y_pos += 34
        show_text(
            display,
            "Show Frame:",
            self.base_to_display_rect((10, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )
        show_text(
            display,
            "Play Button Sounds:",
            self.base_to_display_rect((410, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        _y_pos += 34
        show_text(
            display,
            "Show Scan Lines:",
            self.base_to_display_rect((10, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )
        show_text(
            display,
            "Play Keyboard Sounds:",
            self.base_to_display_rect((410, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )
        _y_pos += 34
        show_text(
            display,
            "Play Ambient Sounds:",
            self.base_to_display_rect((410, _y_pos, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        pygame.draw.rect(
            display,
            layout_config.colour,
            self.base_to_display_rect((4, 525, self.rect[2] - 8, 38)),
            1,
        )

        show_text(
            display,
            "Streaming mode:",
            self.base_to_display_rect((10, 539, 80, 30)),
            layout_config.font,
            colour=layout_config.colour,
            centered=False,
        )

        pygame.draw.rect(
            display,
            layout_config.colour,
            self.base_to_display_rect((0, 567, self.rect[2], 30)),
            border_bottom_left_radius=layout_config.corner_radius,
            border_bottom_right_radius=layout_config.corner_radius,
        )

        show_text(
            display,
            "To save layout options press crtl-l",
            self.base_to_display_rect((0, 569, self.rect[2], 30)),
            layout_config.font,
            colour=c.BLACK,
            centered=True,
        )

    def update_map_position_switches(self) -> None:

        #  Initialise switches.

        _top_left: bool = False
        _bottom_left: bool = False
        _top_middle: bool = False
        _bottom_middle: bool = False
        _top_right: bool = False
        _bottom_right: bool = False

        if layout_config.layout_config["console_layout"]["map_position"] == "LEFT_TOP":
            _top_left = True
        if (
            layout_config.layout_config["console_layout"]["map_position"]
            == "LEFT_BOTTOM"
        ):
            _bottom_left = True
        if (
            layout_config.layout_config["console_layout"]["map_position"]
            == "MIDDLE_TOP"
        ):
            _top_middle = True
        if (
            layout_config.layout_config["console_layout"]["map_position"]
            == "MIDDLE_BOTTOM"
        ):
            _bottom_middle = True
        if layout_config.layout_config["console_layout"]["map_position"] == "RIGHT_TOP":
            _top_right = True
        if (
            layout_config.layout_config["console_layout"]["map_position"]
            == "RIGHT_BOTTOM"
        ):
            _bottom_right = True

        #  UPdate switches.

        self.map_top_left_switch.update_switch(
            self.base_to_display_rect((240, 38, 130, 30)),
            self.set_map_top_left,
            "Top-Left",
            _top_left,
            False,
        )
        self.map_bottom_left_switch.update_switch(
            self.base_to_display_rect((240, 68, 130, 30)),
            self.set_map_bottom_left,
            "Bottom-Left",
            _bottom_left,
            False,
        )
        self.map_top_middle_switch.update_switch(
            self.base_to_display_rect((370, 38, 130, 30)),
            self.set_map_top_middle,
            "Top-Middle",
            _top_middle,
            False,
        )
        self.map_bottom_middle_switch.update_switch(
            self.base_to_display_rect((370, 68, 130, 30)),
            self.set_map_bottom_middle,
            "Bottom-Middle",
            _bottom_middle,
            False,
        )
        self.map_top_right_switch.update_switch(
            self.base_to_display_rect((500, 38, 130, 30)),
            self.set_map_top_right,
            "Top-Right",
            _top_right,
            False,
        )
        self.map_bottom_right_switch.update_switch(
            self.base_to_display_rect((500, 68, 130, 30)),
            self.set_map_bottom_right,
            "Bottom-Right",
            _bottom_right,
            False,
        )

        self.status_left.update_switch(
            self.base_to_display_rect((240, 103, 130, 30)),
            self.set_status_left,
            "Left",
            not layout_config.status_right_flag,
            False,
        )
        self.status_right.update_switch(
            self.base_to_display_rect((370, 103, 130, 30)),
            self.set_status_right,
            "Right",
            layout_config.status_right_flag,
            False,
        )

        self.terminal_left.update_switch(
            self.base_to_display_rect((240, 138, 130, 30)),
            self.set_terminal_left,
            "Left",
            not layout_config.terminal_right_flag,
            False,
        )
        self.terminal_right.update_switch(
            self.base_to_display_rect((370, 138, 130, 30)),
            self.set_terminal_right,
            "Right",
            layout_config.terminal_right_flag,
            False,
        )

        self.minimap_top.update_switch(
            self.base_to_display_rect((240, 173, 130, 30)),
            self.set_minimap_top,
            "Top",
            layout_config.minimap_top_flag,
            False,
        )
        self.minimap_bottom.update_switch(
            self.base_to_display_rect((370, 173, 130, 30)),
            self.set_minimap_bottom,
            "Bottom",
            not layout_config.minimap_top_flag,
            False,
        )

        self.hold_top.update_switch(
            self.base_to_display_rect((240, 208, 130, 30)),
            self.set_hold_top,
            "Top",
            layout_config.hold_top_flag,
            False,
        )
        self.hold_bottom.update_switch(
            self.base_to_display_rect((370, 208, 130, 30)),
            self.set_hold_bottom,
            "Bottom",
            not layout_config.hold_top_flag,
            False,
        )

    def update_colour_sliders(self) -> None:

        self.red_slider.update_slider(
            self.base_to_display_rect((238, 250, 520, 30)),
            self.set_red_level,
            layout_config.colour[0],
        )

        self.green_slider.update_slider(
            self.base_to_display_rect((238, 280, 520, 30)),
            self.set_green_level,
            layout_config.colour[1],
        )

        self.blue_slider.update_slider(
            self.base_to_display_rect((238, 310, 520, 30)),
            self.set_blue_level,
            layout_config.colour[2],
        )

    def update_misc_switches(self) -> None:

        _corners: bool = False
        if layout_config.corner_radius != 0:
            _corners = True

        self.curved_corner_toggle.update_switch(
            self.base_to_display_rect((240, 352, 130, 30)),
            self.toggle_corner_radius,
            "",
            _corners,
            False,
        )

        self.background_toggle.update_switch(
            self.base_to_display_rect((240, 386, 130, 30)),
            self.toggle_background,
            "",
            layout_config.background_flag,
            False,
        )

        self.frame_toggle.update_switch(
            self.base_to_display_rect((240, 420, 130, 30)),
            self.toggle_frame,
            "",
            layout_config.frame_flag,
            False,
        )

        self.scan_lines_toggle.update_switch(
            self.base_to_display_rect((240, 454, 130, 30)),
            self.toggle_scan_lines,
            "",
            layout_config.scanlines_flag,
            False,
        )

    def update_sound_switches(self) -> None:

        self.alarm_sounds_toggle.update_switch(
            self.base_to_display_rect((628, 352, 130, 30)),
            self.toggle_alarm_sounds,
            "",
            layout_config.alarm_sound_flag,
            False,
        )

        self.scanner_sounds_toggle.update_switch(
            self.base_to_display_rect((628, 386, 130, 30)),
            self.toggle_scanner_sounds,
            "",
            layout_config.scanner_sound_flag,
            False,
        )

        self.button_sounds_toggle.update_switch(
            self.base_to_display_rect((628, 420, 130, 30)),
            self.toggle_button_sounds,
            "",
            layout_config.button_sound_flag,
            False,
        )

        self.keyboard_sounds_toggle.update_switch(
            self.base_to_display_rect((628, 454, 130, 30)),
            self.toggle_keyboard_sounds,
            "",
            layout_config.key_sound_flag,
            False,
        )

        self.ambient_sounds_toggle.update_switch(
            self.base_to_display_rect((628, 488, 130, 30)),
            self.toggle_ambient_sounds,
            "",
            layout_config.ambient_sound_flag,
            False,
        )

    def update_streamer_switches(self) -> None:

        self.streamer_mode_toggle.update_switch(
            self.base_to_display_rect((240, 529, 130, 30)),
            self.toggle_streamer_mode,
            "",
            layout_config.streamer_flag,
            False,
        )

    #  Switch and slider callbacks for actually setting values in layout_config.

    def set_map_top_left(self) -> None:
        layout_config.update_pane_positions(layout_config.layout_config, "LEFT_TOP")

    def set_map_bottom_left(self) -> None:
        layout_config.update_pane_positions(layout_config.layout_config, "LEFT_BOTTOM")

    def set_map_top_middle(self) -> None:
        layout_config.update_pane_positions(layout_config.layout_config, "MIDDLE_TOP")

    def set_map_bottom_middle(self) -> None:
        layout_config.update_pane_positions(
            layout_config.layout_config, "MIDDLE_BOTTOM"
        )

    def set_map_top_right(self) -> None:
        layout_config.update_pane_positions(layout_config.layout_config, "RIGHT_TOP")

    def set_map_bottom_right(self) -> None:
        layout_config.update_pane_positions(layout_config.layout_config, "RIGHT_BOTTOM")

    def set_status_left(self) -> None:
        layout_config.update_status_right_flag(layout_config.layout_config, False)

    def set_status_right(self) -> None:
        layout_config.update_status_right_flag(layout_config.layout_config, True)

    def set_terminal_left(self) -> None:
        layout_config.update_terminal_right_flag(
            layout_config.layout_config,
            False,
        )

    def set_terminal_right(self) -> None:
        layout_config.update_terminal_right_flag(
            layout_config.layout_config,
            True,
        )

    def set_minimap_top(self) -> None:
        layout_config.update_minimap_top_flag_value(
            layout_config.layout_config,
            True,
        )

    def set_minimap_bottom(self) -> None:
        layout_config.update_minimap_top_flag_value(
            layout_config.layout_config,
            False,
        )

    def set_hold_top(self) -> None:
        layout_config.update_hold_top_flag_value(
            layout_config.layout_config,
            True,
        )

    def set_hold_bottom(self) -> None:
        layout_config.update_hold_top_flag_value(
            layout_config.layout_config,
            False,
        )

    def set_red_level(self) -> None:
        _colour: tuple[int, int, int] = layout_config.colour
        _new_colour: tuple[int, int, int] = (
            int(self.red_slider.value),
            _colour[1],
            _colour[2],
        )
        layout_config.update_colour_value(layout_config.layout_config, _new_colour)

    def set_green_level(self) -> None:
        _colour: tuple[int, int, int] = layout_config.colour
        _new_colour: tuple[int, int, int] = (
            _colour[0],
            int(self.green_slider.value),
            _colour[2],
        )
        layout_config.update_colour_value(layout_config.layout_config, _new_colour)

    def set_blue_level(self) -> None:
        _colour: tuple[int, int, int] = layout_config.colour
        _new_colour: tuple[int, int, int] = (
            _colour[0],
            _colour[1],
            int(self.blue_slider.value),
        )
        layout_config.update_colour_value(layout_config.layout_config, _new_colour)

    def toggle_corner_radius(self) -> None:
        if layout_config.corner_radius == 15:
            layout_config.update_corner_radius_value(
                layout_config.layout_config,
                0,
            )
        else:
            layout_config.update_corner_radius_value(
                layout_config.layout_config,
                15,
            )

    def toggle_background(self) -> None:
        layout_config.update_background_flag_value(
            layout_config.layout_config,
            not layout_config.background_flag,
        )

    def toggle_frame(self) -> None:
        layout_config.update_frame_flag_value(
            layout_config.layout_config,
            not layout_config.frame_flag,
        )

    def toggle_scan_lines(self) -> None:
        layout_config.update_scanlines_flag_value(
            layout_config.layout_config,
            not layout_config.scanlines_flag,
        )

    def toggle_alarm_sounds(self) -> None:
        layout_config.update_alarm_sound_flag_value(
            layout_config.layout_config,
            not layout_config.alarm_sound_flag,
        )

    def toggle_scanner_sounds(self) -> None:
        layout_config.update_scanner_sound_flag_value(
            layout_config.layout_config,
            not layout_config.scanner_sound_flag,
        )

    def toggle_button_sounds(self) -> None:
        layout_config.update_button_sound_flag_value(
            layout_config.layout_config,
            not layout_config.button_sound_flag,
        )

    def toggle_keyboard_sounds(self) -> None:
        layout_config.update_key_sound_flag_value(
            layout_config.layout_config,
            not layout_config.key_sound_flag,
        )

    def toggle_ambient_sounds(self) -> None:
        layout_config.update_ambient_sound_flag_value(
            layout_config.layout_config,
            not layout_config.ambient_sound_flag,
        )
        if layout_config.ambient_sound_flag is True:
            layout_config.ambient_sound.play(loops=-1)
        else:
            layout_config.ambient_sound.stop()

    def toggle_streamer_mode(self) -> None:
        layout_config.update_streamer_flag_value(
            layout_config.layout_config,
            not layout_config.streamer_flag,
        )

    def play_key_sound(self) -> None:
        if layout_config.key_sound_flag is True:
            layout_config.key_sound.play()
