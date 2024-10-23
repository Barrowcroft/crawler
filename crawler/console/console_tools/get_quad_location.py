#  get_quad_location is a method to get the location of the crawler in the current quadrant on the map.

from functools import cache
from math import floor

import crawler.constants as c


@cache
def get_quad_location(position: tuple[int, int]) -> str:
    """get_quad_location

    get_quad_location is a method to get the location of the crawler in the current quadrant on the map.
    Each quadrant is a square of 10x10 locations on the map.
    Each location is a 64x64 pixel square in the quadrant.

    Args:
        crawler (Crawler): crawler to find quadrant location of.

    Returns:
        str: string with quadrant location of crawler.
    """
    _x: int = ((floor(position[0] / c.MAP_TILE_SIZE)) % 10) + 1
    _y: int = ((floor(position[1] / c.MAP_TILE_SIZE)) % 10) + 1

    return f"[Quad. Loc. {_x}:{_y}]"
