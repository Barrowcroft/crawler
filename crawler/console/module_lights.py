#  The ModuleLights class.

from typing import Callable, Optional

import pygame

import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.module_light import ModuleLight
from crawler.console.console_tools.get_lights_texts import get_lights_texts
from crawler.console.console_tools.show_text import show_text


class ModuleLights(Base):
    """ModuleLights

    The ModuleLights class.

    Args:
        Base: The ModuleLights class subclasses the Base class.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(
        self,
    ) -> None:
        """__init__

        Initialises the ModuleLights.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise the blink_flag and beep variables.

        self.blink_flag: bool = False
        self.request_beep: bool = False

        #  Create module lights and buttons.

        self.module_lights = [ModuleLight() for _ in range(6)]

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.
        Coordinates the handling of events by other classes.

        Args:
            event (pygame.event.Event): event to handle.
        """
        ...

    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for _module_light in self.module_lights:
                _module_light.checkClick(event)

        if event.type == pygame.MOUSEMOTION:
            for _module_light in self.module_lights:
                _module_light.checkHover(event)

    def update_module_lights(
        self,
        rect: tuple[int, int, int, int],
        module_texts: list[tuple[str, str, str]] = [],
        module_levels: list[int] = [],
        module_percent: list[int] = [],
        module_status: list[str] = [],
        actions: list[Optional[Callable[[], None]]] = [],
        signal_flag: bool = False,
        blink_flag: bool = False,
        crawler_id: str = "",
    ) -> None:
        """update_module_lights

        Updates the ModuleLights.

        Args:
            rec (tuple[int, int, int, int]): the position and size of the ModuleLights.
            module_light_texts (list[tuple[str, str, str]): the texts to display in the ModuleLights. Defaults to and empty list.
            module_light_levels (list[int]): the light levels (aka. colour) of the ModuleLights. Defaults to an empty list.
            module_light_percent (list[int]): the health percent of the ModuleLights. Defaults to an empty list.
            module_light_status (list[str]): the status of the ModuleLights. Defaults to an empty list.
            signal_flag (bool): indications if there is a signal. Defaults to True.
            blink_flag (bool): indicates if the lights are in blink_flag cycle. Defauls to False.
            crawler_id: (str): Id of the current crawler.
        """

        #  Save parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.module_light_levels: list[int] = module_levels
        self.module_light_status: list[str] = module_status
        self.signal_flag: bool = signal_flag
        self.crawler_id: str = crawler_id

        #  Create light texts.

        _module_texts = [_text[0] for _text in module_texts]
        _module_light_texts: list[str] = get_lights_texts(_module_texts, module_percent)

        #  Update Base superclass.

        super().update_base(
            rect,
            colour=layout_config.colour,
            corner_radius=layout_config.corner_radius,
            bar=True,
        )

        # Update module lights.

        for index, light in enumerate(self.module_lights):

            if index < len(_module_light_texts):

                light.update_module_light(
                    self.base_to_display_rect((4, 34 + (index * 70), 272, 66)),
                    texts=(
                        _module_light_texts[index],
                        f"{module_texts[index][1]}",
                        f"Level {module_texts[index][2]}",
                    ),
                    level=module_levels[index],
                    percent=module_percent[index],
                    status=module_status[index],
                    occupied=True,
                    index=index,
                    max=len(self.module_lights),
                    blink_flag=blink_flag,
                    action=actions[index],
                )

            else:

                #  Unoccupied light.

                light.update_module_light(
                    self.base_to_display_rect((4, 34 + (index * 70), 272, 66)),
                    texts=("", "", ""),
                    level=0,
                    percent=0,
                    status="",
                    occupied=False,
                    index=index,
                    max=len(self.module_lights),
                    blink_flag=blink_flag,
                    action=None,
                )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the ModuleLights class.

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

            #  Render personnel lights and buttons.

            for light in self.module_lights:
                light.render(display)

        #  Show pane text.

        show_text(
            display,
            f"{self.crawler_id} Modules",
            self.base_to_display_rect((0, 0, self.rect[2], 30)),
            layout_config.font,
            (0, 0, 0),
            False,
            15,
            8,
        )

        #  If any of the levels are a level 3 then we need to request beep.

        self.request_beep = False

        for _level in self.module_light_levels:
            if _level == 3:
                self.request_beep = True
                break

        for _status in self.module_light_status:
            if _status != "ONLINE":
                self.request_beep = True
                break
