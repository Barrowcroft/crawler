#  show_light_text_two_line is a method to show two lines of text centered on a given surface.

import pygame

WHITE = (255, 255, 255)


def show_light_text_two_lines(
    display: pygame.Surface,
    text: tuple[str, str],
    rect: tuple[int, int, int, int],
    font: pygame.font.Font,
    colour: tuple[int, int, int] = WHITE,
    x_offset: int = 0,
    y_offset: int = 0,
) -> None:
    """show_light_text_two_lines

    show_light_text_two_line is a method to show two lines of text centered on a given surface.

    Args:
        display (pygame.Surface): display on to which to render text.
        text (tuple[str,str]): text to render.
        rect (tuple[int, int, int, int]): rectangle in to which to display text.
        font (pygame.font.Font); font to use to render text.
        colour tuple[int,int,int]: colour of text to render. Defaults to layout_config.colour.
        x_offset (int): x offset of text on surface. Defaults to 0.
        y_offset (int): y offset of text on surface. Defaults to 0.
    """

    #  Render the text on the surface.

    _text_object_1: pygame.Surface = font.render(text[0], True, colour)
    _text_object_2: pygame.Surface = font.render(text[1], True, colour)

    #  Get width and height of surface and center the text's rectangle.

    if text[1] == "":
        _multiline_offset: int = 0
    else:
        _multiline_offset: int = 9

    _left, _top, _width, _height = rect

    _text_rect_1: pygame.Rect = _text_object_1.get_rect(
        center=(
            _left + int(_width / 2) + x_offset,
            _top + int(_height / 2) + y_offset - _multiline_offset,
        )
    )

    _text_rect_2: pygame.Rect = _text_object_2.get_rect(
        center=(
            _left + int(_width / 2) + x_offset,
            _top + int(_height / 2) + y_offset + _multiline_offset,
        )
    )

    #  Blit the text to the surface.

    display.blit(_text_object_1, _text_rect_1)
    display.blit(_text_object_2, _text_rect_2)
