#  show_light_text is a method to show text centered on a given surface.

import pygame

WHITE = (255, 255, 255)


def show_light_text(
    display: pygame.Surface,
    text: str,
    rect: tuple[int, int, int, int],
    font: pygame.font.Font,
    colour: tuple[int, int, int] = WHITE,
    x_offset: int = 0,
    y_offset: int = 0,
) -> None:
    """show_light_text

    show_light_text is a method to show text centered on a given surface.

    Args:
        display (pygame.Surface): display on to which to render text.
        text (str): text to render.
        rect (tuple[int, int, int, int]): rectangle in to which to display text.
        font (pygame.font.Font); font to use to render text.
        colour tuple[int,int,int]: colour of text to render. Defaults to white.
        x_offset (int): x offset of text on surface. Defaults to 0.
        y_offset (int): y offset of text on surface. Defaults to 0.
    """

    #  Render the text on the surface.

    _text_object_1: pygame.Surface = font.render(text, True, colour)

    #  Get width and height of surface and center the text's rectangle.

    _left, _top, _width, _height = rect

    _text_rect_1: pygame.Rect = _text_object_1.get_rect(
        center=(
            _left + int(_width / 2) + x_offset,
            _top + int(_height / 2) + y_offset,
        )
    )

    #  Blit the text to the surface.

    display.blit(_text_object_1, _text_rect_1)
