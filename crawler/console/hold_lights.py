#  The HoldLights class.

import pygame

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.hold_light import HoldLight
from crawler.console.console_tools.get_lights_texts import get_lights_texts
from crawler.console.console_tools.show_text import show_text


class HoldLights(Base):
    """HoldLights

    The HoldLights class.

    Args:
        Base: The HoldLights class subclasses the Base class.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(
        self,
    ) -> None:
        """__init__

        Initialises the HoldLights.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise crawler id.

        self.crawler_id: str = ""

        #  Initialise the blink_flag and beep variables.

        self.blink_flag: bool = False
        self.request_beep: bool = False

        #  Create personnel lights.

        self.personnel_lights = [HoldLight() for _ in range(10)]
        self.showing_personnel = True

        #  Create salvage lights.

        self.salvage_lights = [HoldLight() for _ in range(10)]

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        if event.type == pygame.KEYDOWN:
            _keys = pygame.key.get_pressed()

            #  This key press handles switching between displaying the personnel in the hold pane
            #  or displaying the salvaged items.

            if (_keys[pygame.K_LCTRL] or _keys[pygame.K_RCTRL]) and _keys[pygame.K_h]:
                if self.showing_personnel == True:
                    self.showing_personnel = False
                else:
                    self.showing_personnel = True

    def update_hold_lights(
        self,
        rect: tuple[int, int, int, int],
        personnel_texts: list[tuple[str, str]] = [],
        personnel_levels: list[int] = [],
        personnel_percent: list[int] = [],
        personnel_status: list[str] = [],
        salvage_texts: list[tuple[str, str]] = [],
        salvage_levels: list[int] = [],
        salvage_percent: list[int] = [],
        salvage_status: list[str] = [],
        blink_flag: bool = False,
        signal_flag: bool = False,
        crawler_id: str = "",
    ) -> None:
        """update_hold_lights

        Updates the HoldLights.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the HoldLights.
            personnel_light_texts (list[tuple[str,str]]): the texts to display in the personnel entries of HoldLights. Defaults to and empty list.
            personnel_light_levels (list[int]): the light levels (aka. colour) ofthe personnel entries of HoldLights. Defaults to an empty list.
            personnel_light_percent (list[int]): the percent of the personnel entries of HoldLights. Defaults to an empty list.
            personnel_light_status (list[str]): the status of the personnel entries of HoldLights. Defaults to an empty list.
            salvage_light_texts (list[tuple[str, str]]): the texts to display in the salvage entries of HoldLights. Defaults to an empty list.
            salvage_light_levels (list[int]): the light levels (aka. colour) of the salvage entries of HoldLights. Defaults to an empty list.
            salvage_light_percent (list[int]): the health percent of the salvage entries of HoldLights. Defaults to an empty list.
            salvage_light_status (list[int]): the status of the salvage entries of HoldLights. Defaults to an empty list.
            signal_flag (bool): indications if there is a signal. Defaults to True.
            blink_flag (bool): indicates if the lights are in blink_flag cycle. Defauls to False.
            crawler_id: (str): Id of the current crawler.
        """

        #  Save parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.personnel_light_levels: list[int] = personnel_levels
        self.personnel_light_status: list[str] = personnel_status
        self.salvage_light_levels: list[int] = salvage_levels
        self.salvage_light_status: list[str] = salvage_status
        self.signal_flag: bool = signal_flag
        self.crawler_id: str = crawler_id

        #  Create personnel light texts.

        _personnel_texts = [_text[0] for _text in personnel_texts]
        _personnel_light_texts: list[str] = get_lights_texts(
            _personnel_texts, personnel_percent
        )

        #  Create salvage light texts.

        _salvage_texts = [_text[0] for _text in salvage_texts]
        _salvage_light_texts: list[str] = get_lights_texts(
            _salvage_texts, salvage_percent
        )

        #  Update superclass.

        super().update_base(
            rect,
            colour=layout_config.colour,
            corner_radius=layout_config.corner_radius,
            bar=True,
        )

        # Update personnel lights.

        for index, light in enumerate(self.personnel_lights):
            if index < len(_personnel_light_texts):

                light.update_hold_light(
                    self.base_to_display_rect((4, 34 + (index * 49), 272, 45)),
                    texts=(
                        _personnel_light_texts[index],
                        f"({personnel_texts[index][1]})",
                    ),
                    level=personnel_levels[index],
                    percent=personnel_percent[index],
                    status=personnel_status[index],
                    occupied=True,
                    personnel=True,
                    index=index,
                    max=len(self.personnel_lights),
                    blink_flag=blink_flag,
                )

            else:

                #  Unoccupied light.

                light.update_hold_light(
                    self.base_to_display_rect((4, 34 + (index * 49), 272, 45)),
                    texts=("", ""),
                    level=0,
                    percent=0,
                    status="ONLINE",
                    occupied=False,
                    personnel=True,
                    index=index,
                    max=len(self.personnel_lights),
                    blink_flag=blink_flag,
                )

        # Update salvage lights.

        for index, light in enumerate(self.salvage_lights):
            if index < len(_salvage_light_texts):

                light.update_hold_light(
                    self.base_to_display_rect((4, 34 + (index * 49), 272, 45)),
                    texts=(
                        _salvage_light_texts[index],
                        f"({salvage_texts[index][1]})",
                    ),
                    level=salvage_levels[index],
                    percent=salvage_percent[index],
                    status=salvage_status[index],
                    occupied=True,
                    personnel=False,
                    index=index,
                    max=len(self.salvage_lights),
                    blink_flag=blink_flag,
                )

            else:

                #  Unoccupied light.

                light.update_hold_light(
                    self.base_to_display_rect((4, 34 + (index * 49), 272, 45)),
                    texts=("", ""),
                    level=0,
                    percent=0,
                    status="ONLINE",
                    occupied=False,
                    personnel=False,
                    index=index,
                    max=len(self.salvage_lights),
                    blink_flag=blink_flag,
                )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the HoldLights class.

        Args:
            display (pygame.event.Event): display on which to render.
        """

        #  Render the Base superclass.

        super().render(display)

        _showing: str = ""
        if self.signal_flag is False:
            show_text(
                display,
                "No signal",
                self.rect,
                layout_config.font,
                self.colour,
            )
        else:

            #  Render lights.

            if self.showing_personnel == True:

                #  Render personnel lights.

                for light in self.personnel_lights:
                    light.render(display)

                _showing: str = "[Personnel]"

            else:
                #  Render salvage lights.

                for light in self.salvage_lights:
                    light.render(display)

                _showing: str = "[Salvage]"

        #  Show pane text.

        _message1: str = f"{self.crawler_id} Hold"
        _message2: str = f"{_showing}"

        show_text(
            display,
            f"{_message1:<10} {_message2:>16}",
            self.base_to_display_rect((0, 0, self.rect[2], 30)),
            layout_config.font,
            c.BLACK,
            False,
            15,
            8,
        )

        #  If any of the levels are a level 3 then we need to request beep.

        self.request_beep = False
        for _level in self.personnel_light_levels:
            if _level == 3:
                self.request_beep = True
                break
        for _level in self.salvage_light_levels:
            if _level == 3:
                self.request_beep = True
                break

        for _status in self.personnel_light_status:
            if _status != "ONLINE":
                self.request_beep = True
                break
        for _status in self.salvage_light_status:
            if _status != "ONLINE":
                self.request_beep = True
                break
