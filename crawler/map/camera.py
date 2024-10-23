#  The Camera class.

from pygame import Rect, sprite

import crawler.constants as c
from crawler.config import layout_config


class Camera:
    """Camera

    The 'Camera' is a mechanism to adjust the position of the sprite to
    allow for scrolling the map.
    """

    def __init__(self, size: tuple[int, int]) -> None:
        """__init__

        Initialises the camera.

        Args:
            size (tuple[int, int]): size of camera.
        """

        #  Create the camera rectanle

        self._width: int = size[0]
        self._height: int = size[1]
        self._camera: Rect = Rect(0, 0, self._width, self._height)

    # HELPER METHODS ##########################################################

    def apply(self, entity: sprite.Sprite) -> Rect:
        """apply

        Adjusts the position of the sprite with respect to the camera.

        Args:
            entity (sprite.Sprite): sprite to adjust the position of.

        Returns:
            _type_: new rectanbgle.
        """

        #  Move the sprite with respect to the camera

        _rect: Rect = entity.rect.move(self._camera.topleft)  #  type: ignore
        return _rect  #  type: ignore

    # MAIN GAMELOOP METHODS ###################################################

    def update(self, position: tuple[int, int]) -> None:
        """update

        Adjusts the camera to the position of the sprite.
        Usually the sprite is the crawler.

        Args:
            target (sprite.Sprite): sprite to adjust camera to.
        """

        #  Get map view size.

        if layout_config.streamer_flag is True:
            _map_view_size = c.MAP_VIEW_SIZE_STREAMING
        else:
            _map_view_size = c.MAP_VIEW_SIZE

        #  Get center of srite

        _x = -(position[0] + 32) + int(_map_view_size[0] / 2)  #  type: ignore
        _y = -(position[1] + 32) + int(_map_view_size[1] / 2)  #  type: ignore

        #  Adjust for map edges

        _x = min(0, _x)  #  type: ignore
        _y = min(0, _y)  #  type: ignore
        _x = max(-(self._width - _map_view_size[0]), _x)
        _y = max(-(self._height - _map_view_size[1]), _y)

        #  Reset camera rectanlge

        self._camera = Rect(_x, _y, self._width, self._height)
