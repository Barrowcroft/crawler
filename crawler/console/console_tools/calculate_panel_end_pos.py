#  calculate_end_pos is a method to calculate the end position of a sliding panel.

from functools import cache

import crawler.constants as c
from crawler.config import layout_config


@cache
def calculate_end_pos(rect: tuple[int, int, int, int], appear: str) -> tuple[int, int]:

    _x_end_pos: int = 0
    _y_end_pos: int = 0

    if layout_config.streamer_flag is True:
        _map_view_size = c.MAP_VIEW_SIZE_STREAMING
    else:
        _map_view_size = c.MAP_VIEW_SIZE

    if appear == "top":
        _x_end_pos = int((_map_view_size[0] - rect[2]) / 2)
        _y_end_pos = 10

    if appear == "bottom":
        _x_end_pos = int((_map_view_size[0] - rect[2]) / 2)
        _y_end_pos = _map_view_size[1] - 70 - rect[3]

    if appear == "left":
        _x_end_pos = 10
        _y_end_pos = int((_map_view_size[1] - rect[3]) / 2)

    if appear == "right":
        _x_end_pos = _map_view_size[0] - rect[2] - 15
        _y_end_pos = int((_map_view_size[1] - rect[3]) / 2)

    return _x_end_pos, _y_end_pos
