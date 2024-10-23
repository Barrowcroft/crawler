#  get_quad_location is a method to get he quadrant of the crawler on the map.

from functools import cache
from math import floor

import crawler.constants as c


@cache
def get_quad(position: tuple[int, int]) -> str:
    """get_quad

    et_quad_location is a method to get he quadrant of the crawler on the map.
    Each quadrant is a square of 10x10 locations on the map.

    Args:
        crawler (Crawler): crawler to find quadrant of.

    Returns:
        str: string with quadrant of crawler.
    """
    _x: int = ((floor(position[0] / c.MAP_TILE_SIZE)) * 10) + 1
    _y: int = ((floor(position[1] / c.MAP_TILE_SIZE)) * 10) + 1

    return f"[Quad. {_x}:{_y}]"
