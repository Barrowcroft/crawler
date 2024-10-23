#  The MapManager creates the Map and Grid and loads the sprites creating them as Objects.

import os
import threading
from typing import Optional

import pygame
import pytmx  # type: ignore

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_tools.show_text import show_text
from crawler.crawler.crawler import Crawler
from crawler.map.camera import Camera
from crawler.map.grid import Grid
from crawler.map.map import Map
from crawler.map.object import Object


class MapManager:
    """MapManager

    The MapManager creates the Map and Grid and loads the sprites creating them as Objects.

    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(self, filename: str, crawlers: list[Crawler]) -> None:
        """__init__

        Initialise the MapManager.

        Args:
            filename (str): the file from which to read the map.
        """

        #  Initialise MapManager variables.

        self.map_alpha = 160
        self.object_alpha = 160
        self.grid_alpha = 80

        self.map_image: Optional[pygame.Surface] = None
        self.mini_map_image: Optional[pygame.Surface] = None
        self.grid_map_image: Optional[pygame.Surface] = None

        self.camera: Camera | None = None
        self.crawlers: list[Crawler] = crawlers

        self.pod_locations: list[tuple[int, int]] = [
            (4000, 4000),
            (8800, 4000),
            (6400, 6400),
            (4000, 8800),
            (8800, 8800),
        ]
        self.salvage_locations: list[tuple[int, int]] = [
            (6400, 4000),
            (4000, 6400),
            (8800, 6400),
            (6400, 8800),
        ]

        #  Set up the sprite gropups.
        #  Objects that have an image will be in the sprite_group.
        #  Objects that are interacted with will be in the object_group.
        #  Some  objects will be in both.

        self.sprite_group: pygame.sprite.Group = pygame.sprite.Group()  # type: ignore
        self.object_group: pygame.sprite.Group = pygame.sprite.Group()  # type: ignore

        self.loaded: bool = False

        #  Set a new thread to create map and grid.

        def thread_function():

            #  Load map data.

            _map_data: pytmx.TiledMap = self.load_map_data(filename)

            #  Create map image loading appropriate images.
            #  This will also create the othe rmap objects (solids, terrain etc.)

            self.map_image = self.create_map(_map_data)

            #  Add the Map as a Sprite to the sprite group.

            Map(self.sprite_group, self.map_image)  # type: ignore

            # #  Create map grid.

            self.grid_map_image = self.create_map_grid(_map_data)

            #  Add the Grid as a Sprite to the sprite group.

            Grid(self.sprite_group, self.grid_map_image)  # type: ignore

            #  Create mini map image.

            self.mini_map_image = self.create_mini_map(self.map_image)

            #  Indicate map is loaded.

            self.loaded = True

            #  Create camera.

            if self.map_image is not None:
                self.camera = Camera(
                    (
                        self.map_image.get_width(),
                        self.map_image.get_height(),
                    )
                )

            #  Add crawlers to sprite group.

            for _crawler in self.crawlers:
                self.sprite_group.add(_crawler)  # type: ignore

        #  Start new thread.

        thread = threading.Thread(target=thread_function)
        thread.start()

    @customlogger.log_trace(customlogger.Levels.INFO)
    def load_map_data(self, filename: str) -> pytmx.TiledMap:

        #  Load the map data from the data file.

        _map_data: pytmx.TiledMap = pytmx.load_pygame(  # type: ignore
            os.path.join(
                "crawler",
                c.DIR_ASSETS,
                c.DIR_MAPS,
                filename,
            ),
            pixelalpha=True,
        )

        return _map_data

    @customlogger.log_trace(customlogger.Levels.INFO)
    def create_map(self, map_data: pytmx.TiledMap) -> pygame.Surface:
        """

        There are two kinds of layers:

            TiledTileLayer is just visible tiles making up the map design.

            TiledObjectGroup represents the objects which can be:

                Visible, i.e. they have associated images and should be displayed; pods, cannisters, spawnpoints etc.
                Invisible, i.e. they acts as triggers or collision points; solids, terrain etc.

        """

        #  Create a surface of the correct size for the map.

        _surface: pygame.Surface = pygame.Surface(
            (
                map_data.width * map_data.tilewidth,
                map_data.height * map_data.tileheight,
            ),
            # pygame.SRCALPHA,
        )

        #  Loop over the layers.

        for layer in map_data.layers:  # type: ignore

            #  Draw tiled layer and create the basic map.

            if isinstance(layer, pytmx.TiledTileLayer):

                #  Get the correct tile image and blit it to the map image surface.

                for _x, _y, _gid in layer:  # type: ignore
                    _tile: pygame.Surface = map_data.get_tile_image_by_gid(_gid)  # type: ignore
                    if _tile:
                        _tile.set_alpha(self.map_alpha)
                        _surface.blit(
                            _tile,
                            (
                                _x * map_data.tilewidth,  # type: ignore
                                _y * map_data.tileheight,  # type: ignore
                            ),
                        )

            #  Loop over the objects on the object layer creating appropriate objects.

            if isinstance(layer, pytmx.TiledObjectGroup):

                for _object in map_data.objects:  # type: ignore

                    if _object.visible == 1:

                        _object_surface: pygame.Surface = pygame.Surface(
                            (
                                c.MAP_TILE_SIZE,
                                c.MAP_TILE_SIZE,
                            ),
                        )

                        _image: pygame.Surface = map_data.get_tile_image_by_gid(_object.id)  # type: ignore

                        _image.set_alpha(self.object_alpha)

                        _object_surface.blit(
                            _image,
                            (
                                0,  # type: ignore
                                0,  # type: ignore
                            ),
                        )
                        _object.properties["type"] = _object.name  # type: ignore
                        Object(
                            [self.sprite_group, self.object_group],  # type: ignore
                            pygame.rect.Rect(
                                _object.x, _object.y, _object.width, _object.height
                            ),
                            _object_surface,
                            _object.properties,  # type: ignore
                        )
                    else:
                        if _object.name is not None and _object.name == "spawnpoint":
                            self.crawlers[
                                int(_object.properties["num"]) - 1  # type: ignore
                            ].position = (
                                _object.x,
                                _object.y,
                            )
                        else:
                            _object.properties["type"] = _object.name  # type: ignore
                            Object(
                                self.object_group,  # type: ignore
                                pygame.rect.Rect(
                                    _object.x, _object.y, _object.width, _object.height
                                ),
                                None,
                                _object.properties,  # type: ignore
                            )

        return _surface

    @customlogger.log_trace(customlogger.Levels.INFO)
    def create_mini_map(self, map: pygame.Surface) -> pygame.Surface:

        #  Scale the map for the mini_map.

        _mini_map = pygame.transform.scale(
            map, (c.MINIMAP_SIZE[0] - 2, c.MINIMAP_SIZE[1] - 2)
        )

        #  Draw grid on mini_map.

        #  NWork out scaled tile size.

        _width_factor: float = (c.MAP_TILES_ACROSS * c.MAP_TILE_SIZE) / (
            c.MAP_TILE_SIZE * 10
        )
        _height_factor: float = (c.MAP_TILES_DOWN * c.MAP_TILE_SIZE) / (
            c.MAP_TILE_SIZE * 10
        )

        _scaled_tens_width = c.MINIMAP_SIZE[0] / _width_factor
        _scaled_tens_height = c.MINIMAP_SIZE[1] / _height_factor

        #  Draw the grid.

        _colour: tuple[int, int, int] = (
            int(layout_config.colour[0] / 5),
            int(layout_config.colour[1] / 5),
            int(layout_config.colour[2] / 5),
        )

        for _col in range(0, c.MINIMAP_SIZE[0], 14):
            pygame.draw.line(
                _mini_map, c.DARK_GRAY, (_col, 0), (_col, c.MINIMAP_SIZE[1]), 1
            )

        for _row in range(0, c.MINIMAP_SIZE[0], 14):
            pygame.draw.line(
                _mini_map, c.DARK_GRAY, (0, _row), (c.MINIMAP_SIZE[0], _row), 1
            )

        return _mini_map

    @customlogger.log_trace(customlogger.Levels.INFO)
    def create_map_grid(self, map_data: pytmx.TiledMap) -> pygame.Surface:

        #  Create a surface of the correct size for the map.

        _surface: pygame.Surface = pygame.Surface(
            (
                map_data.width * map_data.tilewidth,
                map_data.height * map_data.tileheight,
            ),
            pygame.SRCALPHA,
        )

        #  Number of tiles in map.

        _cols: int = c.MAP_TILES_ACROSS
        _rows: int = c.MAP_TILES_DOWN

        #  Draw the grid.

        for _row in range(0, _rows):
            for _col in range(0, _cols):
                _tile = pygame.Surface(
                    (c.MAP_TILE_SIZE, c.MAP_TILE_SIZE), pygame.SRCALPHA
                ).convert_alpha()
                _tile.set_alpha(self.grid_alpha)

                #  Draw grid round each tile.

                pygame.draw.line(_tile, c.GRAY, (0, 0), (5, 0), 1)
                pygame.draw.line(_tile, c.GRAY, (0, 0), (0, 5), 1)
                pygame.draw.line(_tile, c.GRAY, (59, 0), (64, 0), 1)
                pygame.draw.line(_tile, c.GRAY, (0, 59), (0, 64), 1)

                #  Draw a heavier line for every tenth tile.

                if (_col == 0) or (_col % 10 == 0):
                    pygame.draw.line(_tile, c.GRAY, (0, 0), (0, 64), 1)

                if (_row == 0) or (_row % 10 == 0):
                    pygame.draw.line(_tile, c.GRAY, (0, 0), (64, 0), 1)

                #  Add a label to the lower corner of every block of ten tiles.

                if ((_col + 1) % 10 == 0) and ((_row + 1) % 10 == 0):
                    pygame.draw.rect(
                        _tile,
                        c.GRAY,
                        (0, _tile.get_height() - 20, _tile.get_width(), 20),
                    )

                    show_text(
                        _tile,
                        f"{_col+1}:{_row+1}",
                        (0, _tile.get_height() - 20, _tile.get_width(), 20),
                        layout_config.font,
                        c.BLACK,
                        True,
                        y_offset=2,
                    )

                #  Blit the tile.

                _surface.blit(
                    _tile,
                    (
                        _col * c.MAP_TILE_SIZE,
                        _row * c.MAP_TILE_SIZE,
                    ),
                )

        return _surface
