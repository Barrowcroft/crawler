#  The Status class.

import pygame

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.show_text import show_text
from crawler.console.minimap import MiniMap
from crawler.console.system_dials import SystemDials
from crawler.console.system_lights import SystemLights
from crawler.console.warning_lights import WarningLights
from crawler.map.map_manager import MapManager


class Status(Base):
    """Status

    The Status class.

    Args:
        Base: The StatusPane subclasses the Base class.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(
        self,
    ) -> None:
        """__init__

        Initialise the class.

        """
        #  Initialise superclass.

        super().__init__()

        # Create the subpanels.

        self.minimap: MiniMap = MiniMap()
        self.warning_lights: WarningLights = WarningLights()
        self.dials: SystemDials = SystemDials()
        self.system_lights: SystemLights = SystemLights()

    def update_status(
        self,
        dt: float,
        map_manager: MapManager,
        rect: tuple[int, int, int, int],
        crawler_position: tuple[int, int] = (0, 0),
        warning_light_levels: list[int] = [],
        system_light_levels: list[int] = [],
        system_light_percent: list[int] = [],
        system_light_status: list[str] = [],
        dial_light_levels: list[int] = [],
        dial_light_percent: list[int] = [],
        blink_flag: bool = True,
        signal_flag: bool = False,
    ) -> None:
        """update_status

        Updates the Status class paramters.

        Args:
            dt (float): delta time.
            map_manager (MapManager): the map manager to retireve the minimap.
            rect (tuple[int, int, int, int]): the position and size of the Status.
            crawler_position (tuple[int, int]): coordinates of crawler,. Defaults to (0, 0).
            warning_light_levels (list[int]): the light levels (aka. colour) of the WarningLights. Defaults to an empty list.
            system_light_levels (list[int]): the light levels (aka. colour) of the SystemLights. Defaults to an empty list.
            system_light_percent (list[int]): the health percent of the SystemLights. Defaults to an empty list.
            system_light_status (list[str]): thestatus of the SystemLights. Defaults to an empty list.
            dials_light_levels (list[int]): the light levels (aka. colour) of the SystemDials. Defaults to an empty list.
            dials_light_percent (list[int]): the percent of the SystemDials. Defaults to an empty list.
            blink_flag (bool): indicates if the lights are in blink_flag cycle. Defauls to False.
            signal_flag (bool): indications if there is a signal. Defaults to True.
        """
        #  Save Status parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.signal_flag: bool = signal_flag

        #  Update Base superclass.

        super().update_base(
            rect,
            colour=layout_config.colour,
            corner_radius=layout_config.corner_radius,
            bar=True,
        )

        #  Update subcomponents.

        if layout_config.minimap_top_flag == True:
            _minimap_layout = c.STATUS_MINIMAP_TOP_LAYOUT
            _warnings_lights_layout = c.STATUS_WARNING_LIGHTS_TOP_LAYOUT
            _dials_layout = c.STATUS_DIALS_TOP_LAYOUT
            _system_lights_layout = c.STATUS_MODULES_TOP_LAYOUT
        else:
            _minimap_layout = c.STATUS_MINIMAP_BOTTOM_LAYOUT
            _warnings_lights_layout = c.STATUS_WARNING_LIGHTS_BOTTOM_LAYOUT
            _dials_layout = c.STATUS_DIALS_BOTTOM_LAYOUT
            _system_lights_layout = c.STATUS_MODULES_BOTTOM_LAYOUT

        self.minimap.update_minimap(
            dt,
            map_manager.mini_map_image,  #  type: ignore
            self.base_to_display_rect(_minimap_layout),
            crawler_position=crawler_position,
            signal_flag=signal_flag,
        )

        self.warning_lights.update_warning_lights(
            self.base_to_display_rect(_warnings_lights_layout),
            levels=warning_light_levels,
            blink_flag=blink_flag,
            signal_flag=signal_flag,
        )

        self.dials.update_system_dials(
            dt,
            self.base_to_display_rect(_dials_layout),
            levels=dial_light_levels,
            percent=dial_light_percent,
            blink_flag=blink_flag,
            signal_flag=signal_flag,
        )
        self.system_lights.update_system_lights(
            self.base_to_display_rect(_system_lights_layout),
            levels=system_light_levels,
            percent=system_light_percent,
            status=system_light_status,
            blink_flag=blink_flag,
            signal_flag=signal_flag,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the Status class.

        Args:
            display (pygame.event.Event): display on which to render.
        """

        #  Render the Base superclass.

        super().render(display)

        #  Render the subcomponents.

        show_text(
            display,
            "STATUS",
            self.base_to_display_rect((0, 0, self.rect[2], 30)),
            layout_config.font,
            (0, 0, 0),
        )

        self.minimap.render(display)
        self.warning_lights.render(display)
        self.dials.render(display)
        self.system_lights.render(display)
