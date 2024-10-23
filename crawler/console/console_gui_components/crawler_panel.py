#  The PanelWithOneButton class provides a panel
#  that will slide into view from the edge of the map view.

from functools import partial

import pygame

import crawler.constants as c
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.crawler_light import CrawlerLight
from crawler.console.console_tools.calculate_panel_current_pos import \
    calculate_current_pos
from crawler.console.console_tools.calculate_panel_end_pos import \
    calculate_end_pos
from crawler.console.console_tools.calculate_panel_start_pos import \
    calculate_start_pos
from crawler.console.console_tools.show_text import show_text


class CrawlerPanel(Base):
    """CrawlerPanel

    The CrawlerPanel class provides a panel that will slide into view from the edge of the map view.
    Imports the layout_config to obtain layout information.

    Args:
        Base: The CrawlerPanel class subclasses the Base class.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the CrawlerPanel class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise the CrawlerPanel variables.

        self.current_crawler_number = 1
        self.x_current_pos: int = c.PANEL_POS_UNSET
        self.y_current_pos: int = c.PANEL_POS_UNSET
        self.showing: bool = False
        self.footer_message = "Select crawler 1 - 9"

        #  Create crawler lights.

        self.crawler_lights: list[CrawlerLight] = []
        for _ in range(9):
            self.crawler_lights.append(CrawlerLight())

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        #  Crawler selection options:

        if event.type == pygame.KEYDOWN:
            _keys = pygame.key.get_pressed()

            char_keys_pressed: bool = any(_keys[pygame.K_a + i] for i in range(26))

            if _keys[pygame.K_1]:
                self.select_crawler(1)
            elif _keys[pygame.K_2]:
                self.select_crawler(2)
            elif _keys[pygame.K_3]:
                self.select_crawler(3)
            elif _keys[pygame.K_4]:
                self.select_crawler(4)
            elif _keys[pygame.K_5]:
                self.select_crawler(5)
            elif _keys[pygame.K_6]:
                self.select_crawler(6)
            elif _keys[pygame.K_7]:
                self.select_crawler(7)
            elif _keys[pygame.K_8]:
                self.select_crawler(8)
            elif _keys[pygame.K_9]:
                self.select_crawler(9)
            elif (
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            for _module_light in self.crawler_lights:
                _module_light.checkClick(
                    event,
                    layout_config.map_position[0],
                    layout_config.map_position[1] + 30,
                )

        if event.type == pygame.MOUSEMOTION:
            for _module_light in self.crawler_lights:
                _module_light.checkHover(
                    event,
                    layout_config.map_position[0],
                    layout_config.map_position[1] + 30,
                )

    def update_panel(
        self,
        dt: float,
        rect: tuple[int, int, int, int],
        short_reports: list[dict[str, int]],
        appear: str = "top",
        blink_flag: bool = False,
    ) -> None:
        """update_panel

        Updates the CrawlerPanel parameters.

        Args:
            dt (float): delta time.
            rect (tuple[int, int, int, int]): the position and size of the CrawlerPanel.
            short_reports (list[dict[str, int]]): the short module infoe data from the crawlers.
            appear (str): set where the CrawlerPanel appears from. Deafults to "top".
            blink_flag (bool): indicates if the lights are in blink_flag cycle. Defauls to False.
        """
        #  Save parameters.

        self.rect: tuple[int, int, int, int] = rect

        #  Calculate the position of the panel as it moves.

        _x_start_pos: int = 0
        _y_start_pos: int = 0

        if _x_start_pos == 0:
            _x_start_pos, _y_start_pos = calculate_start_pos(rect, appear)

        _x_end_pos: int = 0
        _y_end_pos: int = 0

        if _x_end_pos == 0:
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

        #  Update the lights.

        _selected: bool = True

        for _index, _crawler_light in enumerate(self.crawler_lights):

            _selected = True if _index == self.current_crawler_number - 1 else False

            _crawler_light.update_crawler_light(
                self.base_to_display_rect(
                    (
                        4,
                        34 + (54 * _index),
                        self.rect[2] - 8,
                        50,
                    )
                ),
                texts=(f"CRWLR{_index+1:02}", "", ""),
                report=short_reports[_index],
                selected=_selected,
                blink_flag=blink_flag,
                action=partial(self.select_crawler, _index + 1),
            )

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the CrawlerPanel class.

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
            "Crawlers",
            self.base_to_display_rect((25, 8, 80, 30)),
            layout_config.font,
            colour=c.BLACK,
            centered=False,
        )

        #  Render the lights.

        for _crawler_light in self.crawler_lights:
            _crawler_light.render(subsurface)

        pygame.draw.rect(
            subsurface,
            layout_config.colour,
            (
                self.rect[0],
                self.rect[1] + 519,
                self.rect[2],
                30,
            ),
            border_bottom_left_radius=layout_config.corner_radius,
            border_bottom_right_radius=layout_config.corner_radius,
        )

        #  Draw footer.

        show_text(
            subsurface,
            self.footer_message,
            self.base_to_display_rect((0, self.rect[3] - 30, self.rect[2], 30)),
            layout_config.font,
            colour=c.BLACK,
            centered=True,
        )

    def select_crawler(self, number: int) -> None:
        self.play_key_sound()
        self.current_crawler_number = number
        self.footer_message = f"Selecting CRWLR{number:02}"
        # self.showing = False

    def play_key_sound(self) -> None:
        if layout_config.key_sound_flag is True:
            layout_config.key_sound.play()
