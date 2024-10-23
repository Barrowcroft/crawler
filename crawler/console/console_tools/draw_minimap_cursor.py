#  draw_minimap_curser is a method to draw the cursor on the MiniMap.

import pygame

import crawler.constants as c
from crawler.config import layout_config

#  In this context the cursor is the box on the minimap
#  that represents the view currently displayed in the main map.


def draw_minimap_cursor(
    display: pygame.Surface,
    rect: tuple[int, int, int, int],
    crawler_position: tuple[int, int],
) -> None:
    """draw_minimap_cursor

    draw_minimap_curser is a method to draw the cursor on the MiniMap.

    Args:
        display (pygame.Surface): display on to which to draw.
        rect (tuple[int, int, int, int]): rectangle into which to draw.
        crawler_position (tuple[int, int]): position of crawler.
    """
    #  Get width and height of minimap.

    _minimap_left, _minimap_top, _minimap_width, _minimap_height = rect

    #  Get width and height of map view.

    if layout_config.streamer_flag is True:
        _map_view_width, _map_view_height = c.MAP_VIEW_SIZE_STREAMING
    else:
        _map_view_width, _map_view_height = c.MAP_VIEW_SIZE

    #  Work out scale factors.

    _horizontal_sacle_factor: float = c.MAP_WIDTH / _minimap_height
    _vertical_scale_factor: float = c.MAP_HEIGHT / _minimap_width

    #  Work out the size of the cursor.

    _cursor_width = _map_view_width / 45
    _cursor_height = _map_view_height / 45

    #  Work out the center point for the cursor based on the position of the crawler.

    _x_pos: float = crawler_position[0] / _horizontal_sacle_factor
    _y_pos: float = crawler_position[1] / _vertical_scale_factor

    #  Adjust the center point to avoid collision with map sides.

    if _x_pos < _cursor_width / 2:
        _x_pos = _cursor_width / 2

    if _x_pos > _minimap_width - (_cursor_width / 2):
        _x_pos = _minimap_width - (_cursor_width / 2)

    if _y_pos < _cursor_height / 2:
        _y_pos = _cursor_height / 2

    if _y_pos > _minimap_height - (_cursor_height / 2):
        _y_pos = _minimap_height - (_cursor_height / 2)

    #  Adjust the center point to account for the position of the minimap.

    _x_pos += _minimap_left
    _y_pos += _minimap_top

    #  Create cursor rectangle.

    _rect: pygame.rect.Rect = pygame.rect.Rect(0, 0, _cursor_width, _cursor_height)
    _rect.center = (int(_x_pos), int(_y_pos))

    #  Draw the cursor.

    pygame.draw.rect(display, layout_config.danger_colour, _rect, 1)
