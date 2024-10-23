#  get_abs_location is a method to get the absolute location of the crawler on the map.

from functools import cache
from math import floor

import crawler.constants as c


@cache
def get_abs_location(position: tuple[int, int]) -> str:
    """get_abs_location

    get_abs_location is a method to get the absolute location of the crawler on the map.
    Each location is a 64x64 pixel square on the map.

    Returns:
        str: string with absolute location of crawler.
    """
    _x: int = ((floor(position[0] / c.MAP_TILE_SIZE))) + 1
    _y: int = ((floor(position[1] / c.MAP_TILE_SIZE))) + 1

    return f"[Abs. Loc. {_x}:{_y}]"
