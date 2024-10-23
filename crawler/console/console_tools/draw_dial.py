#  draw_dial is a method to draw a system dial.

import pygame

from crawler.config import layout_config

from .get_light_colour import get_light_colour
from .show_text import show_text


def draw_dial(
    display: pygame.Surface,
    rect: tuple[int, int, int, int],
    text: str = "",
    level: int = 0,
    percent: int = 0,
    blink_flag: bool = False,
) -> None:
    """draw_dial

    draw_dial is a method to draw a system dial.

    Args:
        display (pygame.Surface): the display on which to draw the dial.
        rect (tuple[int, int, int, int]): the rectangle of the dial area on the display.
        text (str, optional): the text to show in the dial. Defaults to "".
        level (int, optional): the level (aka. colour) of the dial. Defaults to 0.
        percent (int, optional): the percenbt of the dial. Defaults to 0.
        blink_flag (bool, optional): indicates if we are in a blink cycle. Defaults to False.
    """

    #  Initialise Dial variables.

    _left = 0
    _top = 0

    #  Get the light colour.

    light_colour: tuple[int, int, int] = get_light_colour(
        level,
        blink_flag,
    )

    #  Draw meter.

    x_start: int = _left + rect[0] + 5
    x_stop: int = _left + rect[0] + rect[2] - 10
    x_25_percent: int = x_start + int((x_stop - x_start) / 4)
    x_50_percent: int = x_start + int((x_stop - x_start) / 2)
    x_75_percent: int = x_start + int((x_stop - x_start) / 4) * 3
    x_100_percent: int = x_start + ((x_stop - x_start))

    y_top: int = _top + rect[1] + 5
    y_bottom: int = _top + rect[1] + 25

    pygame.draw.line(
        display,
        light_colour,
        (x_start, _top + rect[1] + 15),
        (x_stop, _top + rect[1] + 15),
    )
    pygame.draw.line(
        display,
        light_colour,
        (x_start, y_top),
        (x_start, y_bottom),
    )
    pygame.draw.line(
        display,
        light_colour,
        (x_25_percent, y_top),
        (x_25_percent, y_bottom),
    )
    pygame.draw.line(
        display,
        light_colour,
        (x_50_percent, y_top),
        (x_50_percent, y_bottom),
    )
    pygame.draw.line(
        display,
        light_colour,
        (x_75_percent, y_top),
        (x_75_percent, y_bottom),
    )
    pygame.draw.line(
        display,
        light_colour,
        (x_100_percent, y_top),
        (x_100_percent, y_bottom),
    )

    #  Draw pointer.

    pivot: tuple[int, int] = (
        x_start + int((x_stop - x_start) / 2),
        _top + rect[1] + rect[3] - 8,
    )

    _value: int = x_start + (int(((x_stop - x_start) / 100) * int(percent)))
    pygame.draw.line(display, light_colour, pivot, (_value, _top + rect[1] + 30), 2)

    #  Draw the text rect.

    pygame.draw.rect(
        display,
        (0, 0, 0),
        (x_start, y_top + rect[3] - 38, 125, 3),
    )
    pygame.draw.rect(
        display,
        light_colour,
        (x_start, y_top + rect[3] - 35, 125, 25),
    )

    #  Draw text.

    show_text(
        display,
        "0",
        (
            x_start + 2,
            y_bottom - 10,
            rect[2],
            rect[3],
        ),
        layout_config.small_font,
        light_colour,
        False,
        0,
        1,
    )
    show_text(
        display,
        "25",
        (
            x_25_percent + 2,
            y_bottom - 10,
            rect[2],
            rect[3],
        ),
        layout_config.small_font,
        light_colour,
        False,
        0,
        1,
    )
    show_text(
        display,
        "50",
        (
            x_50_percent + 2,
            y_bottom - 10,
            rect[2],
            rect[3],
        ),
        layout_config.small_font,
        light_colour,
        False,
        0,
        1,
    )
    show_text(
        display,
        "75",
        (
            x_75_percent + 2,
            y_bottom - 10,
            rect[2],
            rect[3],
        ),
        layout_config.small_font,
        light_colour,
        False,
        0,
        1,
    )

    show_text(
        display,
        f"{text} {percent}%",
        (
            _left + rect[0],
            y_bottom + 22,
            rect[2],
            rect[3],
        ),
        layout_config.small_font,
        (0, 0, 0),
        True,
        0,
        1,
    )
