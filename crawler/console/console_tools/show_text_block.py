#  show_text_block.py is a method to show a text block centered on a given surface.

import pygame

import crawler.constants as c


def show_text_block(
    display: pygame.Surface,
    text: str,
    rect: tuple[int, int, int, int],
    font: pygame.font.Font,
    colour: tuple[int, int, int] = c.WHITE,
    x_offset: int = 0,
    y_offset: int = 0,
) -> None:
    """show_text_block

    Renders a block of text centered on a display.

    Args:
        display (pygame.Surface): display on to which to render text.
        text (str): text to render.
        rect (tuple[int, int, int, int]): rectangle in to which to display text.
        font (pygame.font.Font); font to use to render text.
        colour tuple[int,int,int]: colour of text to render. Defaults to white.
        x_offset (int): x offset of text on surface. Defaults to 0.
        y_offset (int): y offset of text on surface. Defaults to 0.
    """

    #  Split the text into alist of text lines.

    _lines: list[str] = text.split("\n")

    #  Calculate total height of text.

    _total_height: int = len(_lines) * font.get_height()

    #  Calculate the y position to start writing the text

    _width = rect[2]
    _height = rect[3]

    _start_y: int = (_height - _total_height) // 2 + y_offset

    #  Loop over lines of text

    for i, _line in enumerate(_lines):
        #  Render text

        _text: pygame.Surface = font.render(_line, True, colour)  # type: ignore

        #  Center the text's rectangle

        _text_rect: pygame.Rect = _text.get_rect(  # type: ignore
            center=(_width // 2 + x_offset, _start_y + (i * 1.5) * font.get_height())
        )

        #  Blit the text to the surface

        display.blit(_text, _text_rect)  # type: ignore
