#  display_terminal_buffer is a method to show the terminal buffer.

import pygame

import crawler.constants as c
from crawler.config import layout_config
from crawler.console.console_tools.show_text import show_text


def display_terminal_buffer(
    display: pygame.Surface,
    rect: tuple[int, int, int, int],
    buffer: list[tuple[int, str]],
    start: int,
) -> None:
    """display_terminal_buffer

    display_terminal_buffer is a method to show the terminal buffer.

    Args:
        display (pygame.Surface): the surface on which to display the termnal lines.
        rect (tuple[int, int, int, int]): the rect of the terminal area on the display.
        buffer (list[tuple[int, str]]): the bufer of terminal texts.
        start (int): the number of the first item to display.
    """

    #  Get the part of the buffer to actually display.

    _current_buffer: list[tuple[int, str]] = buffer[
        start : start + c.TERMINAL_LINES_TO_SHOW
    ]

    #  Loop over selected part of buffer and display each line in turn.

    for _index, _item in enumerate(_current_buffer):

        #  Get correct colour.

        _colour: tuple[int, int, int] = layout_config.colour
        if _item[0] == 2:
            _colour: tuple[int, int, int] = layout_config.warning_colour
        elif _item[0] == 3:
            _colour: tuple[int, int, int] = layout_config.danger_colour

        #  Display the buffer line.

        show_text(
            display,
            "> " + _item[1],
            rect,
            layout_config.font,
            _colour,
            False,
            10,
            40 + (18 * _index - 1),
        )
