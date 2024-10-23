#  The SystemLights class.

import pygame

import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.system_light import SystemLight
from crawler.console.console_tools.get_lights_texts import get_lights_texts
from crawler.console.console_tools.show_text import show_text


class SystemLights(Base):
    """SystemLights

    The SystemLights class.

    Args:
        Base: The SystemLight class subclasses the Base class.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(
        self,
    ) -> None:
        """__init__

        Initialises the SystemLights.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise lights.

        self.light_texts = [
            "Power Cells",
            "Engine",
            "Cooler",
            "Life Support",
            "Hold",
        ]

        self.light_levels: list[int] = []

        #  Initialise the blink_flag and beep variables.

        self.blink_flag: bool = False
        self.request_beep: bool = False

        #  Create warning lights.

        self.engine_warning_light: SystemLight = SystemLight()
        self.cooler_warning_light: SystemLight = SystemLight()
        self.power_cells_warning_light: SystemLight = SystemLight()
        self.life_support_warning_light: SystemLight = SystemLight()
        self.hold_warning_light: SystemLight = SystemLight()

    def update_system_lights(
        self,
        rect: tuple[int, int, int, int],
        levels: list[int] = [],
        percent: list[int] = [],
        status: list[str] = [],
        blink_flag: bool = False,
        signal_flag: bool = False,
    ) -> None:
        """update_system_lights

        Updates the SystemLights.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the SystemLights.
            levels (list[int]): the light levels (aka. colour) of the SystemLights. Defaults to an empty list.
            percent (list[int]): the percent of the SystemLightss. Defaults to an empty list.
            status (list[str]): the status of the SystemLightss. Defaults to an empty list.
            blink_flag (bool): indicates if the lights are in blink_flag cycle. Defauls to False
            signal_flag (bool): indications if there is a signal. Defaults to True.
        """

        #  Save SystemLights parameters.

        self.rect: tuple[int, int, int, int] = rect
        _light_texts: list[str] = get_lights_texts(self.light_texts, percent)
        self.light_levels: list[int] = levels
        self.light_percent: list[int] = percent
        self.light_status: list[str] = status
        self.blink_flag: bool = blink_flag
        self.signal_flag: bool = signal_flag

        #  Update superclass.

        super().update_base(rect, colour=layout_config.colour)

        #  Update power cells lights.

        self.power_cells_warning_light.update_system_light(
            self.base_to_display_rect((4, 4, 272, 30)),
            _light_texts[0],
            levels[0],
            percent[0],
            status[0],
            # online[0],
            blink_flag,
        )

        #  Update engine lights

        self.engine_warning_light.update_system_light(
            self.base_to_display_rect((4, 38, 272, 30)),
            _light_texts[1],
            levels[1],
            percent[1],
            status[1],
            # online[1],
            blink_flag,
        )

        #  Update cooler lights.

        self.cooler_warning_light.update_system_light(
            self.base_to_display_rect((4, 72, 272, 30)),
            _light_texts[2],
            levels[2],
            percent[2],
            status[2],
            # online[2],
            blink_flag,
        )

        #  Update life support lights.

        self.life_support_warning_light.update_system_light(
            self.base_to_display_rect((4, 106, 272, 30)),
            _light_texts[3],
            levels[3],
            percent[3],
            status[3],
            # online[3],
            blink_flag,
        )

        #  Update hold lights.

        self.hold_warning_light.update_system_light(
            self.base_to_display_rect((4, 140, 272, 30)),
            _light_texts[4],
            levels[4],
            percent[4],
            status[4],
            # online[4],
            blink_flag,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the SystemLights class.

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

            #  Render the lights.

            self.power_cells_warning_light.render(display)
            self.engine_warning_light.render(display)
            self.cooler_warning_light.render(display)
            self.life_support_warning_light.render(display)
            self.hold_warning_light.render(display)

        #  If any of the levels are a level 3 then we need to request beep.

        self.request_beep = False
        for _level in self.light_levels:
            if _level == 3:
                self.request_beep = True
                break

        for _status in self.light_status:
            if _status != "ONLINE":
                self.request_beep = True
                break
