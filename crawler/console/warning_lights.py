#  The WarningLights class.

import pygame

import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.light import Light
from crawler.console.console_tools.show_text import show_text


class WarningLights(Base):
    """WarningLights

    The WarningLights class.

    Args:
        Base: The WarningLights class subclasses the Base class.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(
        self,
    ) -> None:
        """__init__

        Initialises the WarningLights.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise lights.

        self.light_texts = [
            "CELLS",
            "OXYGEN",
            "TERRAIN",
            "HEAT",
            "",
            "",
        ]
        self.light_levels: list[int] = []

        #  Initialise the blink_flag and beep variables.

        self.blink_flag: bool = False
        self.request_alarm: bool = False

        #  Create warning lights.

        self.terrain_warning_light: Light = Light()
        self.cells_warning_light: Light = Light()

        self.heat_warning_light: Light = Light()
        self.oxygen_warning_light: Light = Light()

        self.extra_warning_light_1: Light = Light()
        self.extra_warning_light_2: Light = Light()

    def update_warning_lights(
        self,
        rect: tuple[int, int, int, int],
        levels: list[int] = [],
        blink_flag: bool = False,
        signal_flag: bool = False,
    ) -> None:
        """update_warning_lights

        Updates the WarningLights.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the WarningLights.
            levels (list[int]): the light levels (aka. colour) of the WarningLights. Defaults to an empty list.
            blink_flag (bool): indicates if the lights are in blink_flag cycle. Defauls to False.
            signal_flag (bool): indications if there is a signal. Defaults to True.
        """

        #  Save parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.light_levels: list[int] = levels
        self.blink_flag: bool = blink_flag
        self.signal_flag: bool = signal_flag

        #  Save light levels.

        self.light_levels: list[int] = levels

        #  Update Base superclass.

        super().update_base(rect, colour=layout_config.colour)

        #  Update the lights.

        self.cells_warning_light.update_light(
            self.base_to_display_rect((4, 4, 134, 30)),
            text=self.light_texts[0],
            level=levels[0],
            blink_flag=blink_flag,
        )

        self.oxygen_warning_light.update_light(
            self.base_to_display_rect((142, 4, 134, 30)),
            text=self.light_texts[1],
            level=levels[1],
            blink_flag=blink_flag,
        )

        self.terrain_warning_light.update_light(
            self.base_to_display_rect((4, 38, 134, 30)),
            text=self.light_texts[2],
            level=levels[2],
            blink_flag=blink_flag,
        )

        self.heat_warning_light.update_light(
            self.base_to_display_rect((142, 38, 134, 30)),
            text=self.light_texts[3],
            level=levels[3],
            blink_flag=blink_flag,
        )

        self.extra_warning_light_1.update_light(
            self.base_to_display_rect((4, 72, 134, 30)),
            text=self.light_texts[4],
            level=levels[4],
            blink_flag=blink_flag,
        )
        self.extra_warning_light_2.update_light(
            self.base_to_display_rect((142, 72, 134, 30)),
            text=self.light_texts[5],
            level=levels[5],
            blink_flag=blink_flag,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the WarningLights class.

        Args:
            display (pygame.event.Event): display on which to render.
        """

        #  Render the Base superclass.

        super().render(display)

        if self.signal_flag is False:
            show_text(display, "No signal", self.rect, layout_config.font, self.colour)
        else:

            #  Render the lights.

            self.terrain_warning_light.render(display)
            self.cells_warning_light.render(display)
            self.heat_warning_light.render(display)
            self.oxygen_warning_light.render(display)
            self.extra_warning_light_1.render(display)
            self.extra_warning_light_2.render(display)

        #  If any of the levels are a level 3 then we need to request beep.

        self.request_alarm = False
        for _level in self.light_levels:
            if _level == 3:
                self.request_alarm = True
                break
