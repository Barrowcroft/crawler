#  The Inventory class.

from typing import Callable, Optional

import pygame

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.show_text import show_text
from crawler.console.hold_lights import HoldLights
from crawler.console.module_lights import ModuleLights


class Inventory(Base):
    """Inventory

    The inventory file describes the Inventory class.

    Args:
        Base: The Inventory class subclases the Base class.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(
        self,
    ) -> None:
        """__init__

        Initialises the Inventory.
        """

        #  Initialise the Base superclass.

        super().__init__()

        # Create the HoldLights and ModuleLights subpanels.

        self.hold_lights: HoldLights = HoldLights()
        self.module_lights: ModuleLights = ModuleLights()

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        self.hold_lights.handleKeyEvent(event)

    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        self.module_lights.handleMouseEvent(event)

    def update_inventory(
        self,
        rect: tuple[int, int, int, int],
        personnel_light_texts: list[tuple[str, str]] = [],
        personnel_light_levels: list[int] = [],
        personnel_light_percent: list[int] = [],
        personnel_light_status: list[str] = [],
        salvage_light_texts: list[tuple[str, str]] = [],
        salvage_light_levels: list[int] = [],
        salvage_light_percent: list[int] = [],
        salvage_light_status: list[str] = [],
        module_light_texts: list[tuple[str, str, str]] = [],
        module_light_levels: list[int] = [],
        module_light_percent: list[int] = [],
        module_light_status: list[str] = [],
        module_light_actions: list[Optional[Callable[[], None]]] = [],
        signal_flag: bool = True,
        blink_flag: bool = True,
        crawler_id: str = "",
    ) -> None:
        """update_inventory

        Updates the Inventory.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the Inventory.
            personnel_light_texts (list[tuple[str,str]]): the texts to display in the personnel entries of HoldLights. Defaults to an empty list.
            personnel_light_levels (list[int]): the light levels (aka. colour) of the personnel entries of HoldLights. Defaults to an empty list.
            personnel_light_percent (list[int]): the health percent of the personnel entries of HoldLights. Defaults to an empty list.
            personnel_light_status (list[str]): the status of the personnel entries of HoldLights. Defaults to an empty list.
            salvage_light_texts (list[tuple[str, str]]): the texts to display in the salvage entries of HoldLights. Defaults to an empty list.
            salvage_light_levels (list[int]): the light levels (aka. colour) of the salvage entries of HoldLights. Defaults to an empty list.
            salvage_light_percent (list[int]): the health percent of the salvage entries of HoldLights. Defaults to an empty list.
            salvage_light_status (list[str]): the status of the salvage entries of HoldLights. Defaults to an empty list.
            module_light_texts (list[tuple[str, str,str]]): the texts to display in the ModuleLights. Defaults to an empty list.
            module_light_levels (list[int]): the light levels (aka. colour) of the ModuleLights. Defaults to an empty list.
            module_light_percent (list[int]): the health percent of the ModuleLights. Defaults to an empty list.
            module_light_status (list[str]): the status of the ModuleLights. Defaults to an empty list.
            signal_flag (bool): indicates if there is a signal. Defauls to True.
            blink_flag (bool): indicates if the lights are in blink_flag cycle. Defauls to False.
            crawler_id: (str): Id of the current crawler.
        """
        #  Save Inventory parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.signal_flag: bool = signal_flag

        #  Update superclass.

        super().update_base(
            rect,
            colour=layout_config.colour,
            corner_radius=layout_config.corner_radius,
            bar=True,
        )

        #  Get the layout.

        if layout_config.hold_top_flag == True:
            _hold_layout = c.INVENTORY_HOLD_LAYOUT_TOP
            _module_layout = c.INVENTORY_MODULES_LAYOUT_TOP
        else:
            _hold_layout = c.INVENTORY_HOLD_LAYOUT_BOTTOM
            _module_layout = c.INVENTORY_MODULES_LAYOUT_BOTTOM

        #  Update the HoldLights panel.

        self.hold_lights.update_hold_lights(
            self.base_to_display_rect(_hold_layout),
            personnel_texts=personnel_light_texts,
            personnel_levels=personnel_light_levels,
            personnel_percent=personnel_light_percent,
            personnel_status=personnel_light_status,
            salvage_texts=salvage_light_texts,
            salvage_levels=salvage_light_levels,
            salvage_percent=salvage_light_percent,
            salvage_status=salvage_light_status,
            signal_flag=signal_flag,
            blink_flag=blink_flag,
            crawler_id=crawler_id,
        )

        #  Update the ModuleLights panel.

        self.module_lights.update_module_lights(
            self.base_to_display_rect(_module_layout),
            module_texts=module_light_texts,
            module_levels=module_light_levels,
            module_percent=module_light_percent,
            module_status=module_light_status,
            actions=module_light_actions,
            signal_flag=signal_flag,
            blink_flag=blink_flag,
            crawler_id=crawler_id,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Render the Inventory class.

        Args:
            display (pygame.event.Event): display on which to render.
        """

        #  Render the Base superclass.

        super().render(display)

        #  Render the Inventory class.

        show_text(
            display,
            "INVENTORY",
            self.base_to_display_rect((0, 0, self.rect[2], 30)),
            layout_config.font,
            (0, 0, 0),
        )

        self.hold_lights.render(
            display,
        )
        self.module_lights.render(display)
