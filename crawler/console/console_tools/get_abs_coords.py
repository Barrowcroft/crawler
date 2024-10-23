#  get_abs_coords is a method to get the absolute cooridinates of the crawler on the map.

from functools import cache


@cache
def get_abs_coords(position: tuple[int, int]) -> str:
    """get_abs_coords

    get_abs_coords is a method to get the absolute cooridinates of the crawler on the map.

    Returns:
        str: string with absolute coordinates of crawler.
    """
    return f"[Abs. Co-ords. {position[0]}:{position[1]}]"
