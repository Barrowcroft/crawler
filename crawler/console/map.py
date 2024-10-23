#  The Map class.

import pygame
import pygame.gfxdraw

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.scanlines import Scanlines
from crawler.console.console_tools.get_abs_coords import get_abs_coords
from crawler.console.console_tools.get_abs_location import get_abs_location
from crawler.console.console_tools.get_quad import get_quad
from crawler.console.console_tools.get_quad_location import get_quad_location
from crawler.console.console_tools.show_text import show_text
from crawler.map.map_manager import MapManager


class Map(Base):
    """Map

    The Map class.

    Args:
        Base: The Map class subclases the Base class.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(
        self,
    ) -> None:
        """__init__

        Initialise the Map.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise the Map.

        self.rect: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.colour: tuple[int, int, int] = c.BLACK

        #  Initialise the CRT sanlines.

        self.crt_scanlines: Scanlines = Scanlines()

    def update_map(
        self,
        dt: float,
        map_manager: MapManager,
        rect: tuple[int, int, int, int],
        signal_flag: bool = False,
        scanlines_flag: bool = True,
        satellite_id: str = "",
        crawler_position: tuple[int, int] = (0, 0),
    ) -> None:
        """update_map

        Update the Map.

        Args:
            dt (float): delta time.
            map_manager (MapManager): the map manager to display the map and sprites.
            rect (tuple[int, int, int, int]): the position and size of the Map.
            signal_flag (bool): indicates if there is a signal. Defaults to True.
            scanlines_flag (bool): indicates if scanlines are to be drawn. Defaults to True.
            satellite_id (str): the satelitte id ie. secret password!
            crawler_position (tuple[int, int]): position of crawler on map. Defaults to (0,0).
        """

        #  Create / update a subsurface to display the map.

        if rect != self.rect and rect != (0, 0, 0, 0):
            self.rect: tuple[int, int, int, int] = rect
            self.map_view = pygame.Surface(
                (self.rect[2] - 2, self.rect[3] - 62), pygame.SRCALPHA
            )

        #  Create / update colour conversion.

        if self.colour != layout_config.colour:
            self.colour_view = pygame.Surface(
                (self.rect[2] - 2, self.rect[3] - 62), pygame.SRCALPHA
            )
            self.colour_view.fill(layout_config.colour)
            self.colour = layout_config.colour

        #  Save Map parameters.

        self.map_manager: MapManager = map_manager
        self.signal_flag: bool = signal_flag
        self.scanlines_flag: bool = scanlines_flag
        self.satellite_id: str = satellite_id
        self.crawler_position: tuple[int, int] = crawler_position

        #  Update Base superclass.

        super().update_base(
            rect,
            colour=layout_config.colour,
            corner_radius=layout_config.corner_radius,
            bar=True,
        )

        #  Uppdate the camera.

        if self.map_manager.camera is not None:
            self.map_manager.camera.update(crawler_position)

        #  Update CRT Scanlines.

        if self.scanlines_flag is True:
            self.crt_scanlines.update(
                dt, (rect[0], rect[1] + 30, rect[2], rect[3] - 60)
            )

    def render(  #  type: ignore
        self, display: pygame.Surface, actualFPS: float
    ) -> None:
        """render

        Render the Map.

        Args:
            display (pygame.event.Event): display on which to render.
        """

        super().render(display)

        #  Show text.

        if self.signal_flag is False:
            show_text(
                display,
                "No signal",
                self.rect,
                layout_config.font,
                self.colour,
            )
        else:
            show_text(
                display,
                f"[PROVLD Sat. {self.satellite_id}] :: [Sec: A] - {get_quad(self.crawler_position)} - {get_quad_location(self.crawler_position)} - {get_abs_location(self.crawler_position)} - {get_abs_coords(self.crawler_position)}",
                self.base_to_display_rect((0, 0, self.rect[2], 30)),
                layout_config.font,
                c.BLACK,
                True,
                12,
                3,
            )

            #  Save Map parameters.

            self.actualFPS: float = actualFPS

            if (
                self.map_manager.loaded is True
                and not self.map_view.get_locked()
                and not display.get_locked()
            ):

                self.map_view.fill(c.BLACK)

                # Display the sprites.

                self.map_manager.map_image
                for _sprite in self.map_manager.sprite_group:  # type: ignore

                    if _sprite.name == "crawler":  # type: ignore
                        self.map_view.blit(_sprite.image, self.map_manager.camera.apply(_sprite))  # type: ignore
                    else:
                        self.map_view.blit(_sprite.image, self.map_manager.camera.apply(_sprite), special_flags=pygame.BLEND_MAX)  # type: ignore

                display.blit(self.map_view, (self.rect[0] + 1, self.rect[1] + 31))

                #  Add colour conversion.

                display.blit(
                    self.colour_view,
                    (
                        layout_config.map_position[0] + 1,
                        layout_config.map_position[1] + 30,
                    ),
                    special_flags=pygame.BLEND_MULT,
                )

        #  Render CRT scanlines.

        if self.scanlines_flag is True:
            self.crt_scanlines.render(display)

        #  Render footer.

        pygame.draw.rect(
            display,
            layout_config.colour,
            self.base_to_display_rect((0, self.rect[3] - 30, self.rect[2], 30)),
            border_bottom_left_radius=layout_config.corner_radius,
            border_bottom_right_radius=layout_config.corner_radius,
        )

        show_text(
            display,
            f"OK - FPS {int(actualFPS)}",
            self.base_to_display_rect((0, self.rect[3] - 30, self.rect[2], 30)),
            layout_config.font,
            colour=c.BLACK,
            centered=True,
        )
