#  draw_minimap_scan is a method for drawing the scanner on the MiniMap.

import pygame

import crawler.constants as c
from crawler.config import layout_config


def draw_minimap_scan(
    display: pygame.Surface,
    rect: tuple[int, int, int, int],
    targets: list[tuple[int, int]],
    y_offset: int,
) -> bool:
    """draw_minimap_scan

    Args:
        display (pygame.Surface): the display on to which to render.
        rect (tuple[int, int, int, int]): the rectangle in to which to render.
        warning_colour (tuple[int, int, int]): the colour of the scan lines and targets.
        targets (list[tuple[int, int]]): list of traget for the scanner to find.

    Returns:
        bool: _description_
    """
    #  Get width and height of minimap.

    _minimap_left, _minimap_top, _minimap_width, _minimap_height = rect

    #  Work out scale factors.

    _horizontal_sacle_factor: float = _minimap_width / c.MAP_WIDTH
    _vertical_scale_factor: float = _minimap_width / c.MAP_HEIGHT

    #  Convert target locations to minimap coordinates.

    _new_targets: list[tuple[int, int]] = []

    for _target in targets:
        _new_targets.append(
            (
                int(_target[0] * _horizontal_sacle_factor),
                int(_target[1] * _vertical_scale_factor),
            )
        )

    #  Draw scan line.

    pygame.draw.line(
        display,
        layout_config.warning_colour,
        (_minimap_left + 1, _minimap_top + y_offset),
        (_minimap_left + _minimap_width - 2, _minimap_top + y_offset),
    )

    #  Check for hit of target object, and draw hit indicator.

    for _target in _new_targets:
        if _target[1] <= y_offset:
            pygame.draw.circle(
                display,
                layout_config.warning_colour,
                (_minimap_left + _target[0], _minimap_top + _target[1]),
                2,
            )

    #  If the whole map has been scanned end scanner by returning 'False'

    if y_offset == _minimap_height - 1:
        return False
    else:
        return True
