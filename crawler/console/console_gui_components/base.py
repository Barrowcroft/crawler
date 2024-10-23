#  The Base class is the foundation of all other gui components.

import pygame

from crawler.config import layout_config

BLACK = (0, 0, 0)


class Base:
    """Light

    The Base class is the foundation of all other gui elements.
    Imports the layout_config to obtain layout information.
    """

    def __init__(
        self,
    ) -> None:
        """__init__

        Intialises the Base class.
        """

        self.rect: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.colour: tuple[int, int, int] = BLACK
        self.background_flag: bool = False
        self.frame_flag: bool = True
        self.corner_radius: int = 0
        self.bottom_left_corner_radius: int = 0
        self.bottom_right_corner_radius: int = 0
        self.top_left_corner_radius: int = 0
        self.top_right_corner_radius: int = 0
        self.bar: bool = False

    def update_base(
        self,
        rect: tuple[int, int, int, int],
        colour: tuple[int, int, int] = BLACK,
        background_flag: bool = False,
        frame_flag: bool = True,
        corner_radius: int = 0,
        bottom_left_corner_radius: int = 0,
        bottom_right_corner_radius: int = 0,
        top_left_corner_radius: int = 0,
        top_right_corner_radius: int = 0,
        bar: bool = False,
    ) -> None:
        """update_base

        Updates the Base parameters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the Base.
            colour (tuple[int, int, int]): the colour of the Button. Defaults to BLACK.
            background_flag (bool): indicates if the background is to be filled. Defaults to False.
            frame_flag (bool): indicates if a frame is to be drawn. Defaults to True.
            corner_radus (int): radius of frame corners. Defaults to 0.
            bottom_left_corner_radius (int): radius of frame corners. Defaults to 0.
            bottom_right_corner_radius (int): radius of frame corners. Defaults to 0.
            top_left_corner_radius (int): radius of frame corners. Defaults to 0.
            top_right_corner_radius (int): radius of frame corners. Defaults to 0.
            bar (bool): indicates if a title bar is to be be drawn. Defaults to False.
        """
        #  Save parameters.

        self.rect = rect
        self.colour = colour
        self.background_flag = background_flag
        self.frame_flag = frame_flag
        self.corner_radius = corner_radius
        self.bar = bar

        #  The corner value is set for the whole by the corner_radius value
        #  but can be overriden by setting a value for a particular corner.

        if bottom_left_corner_radius != 0:
            self.bottom_left_corner_radius = bottom_left_corner_radius
        else:
            self.bottom_left_corner_radius = self.corner_radius

        if bottom_right_corner_radius != 0:
            self.bottom_right_corner_radius = bottom_right_corner_radius
        else:
            self.bottom_right_corner_radius = self.corner_radius

        if top_left_corner_radius != 0:
            self.top_left_corner_radius = top_left_corner_radius
        else:
            self.top_left_corner_radius = self.corner_radius

        if top_right_corner_radius != 0:
            self.top_right_corner_radius = top_right_corner_radius
        else:
            self.top_right_corner_radius = self.corner_radius

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the base.

        Args:
            display (pygame.Surface): display on which to render.
        """

        # Clear surface.

        pygame.draw.rect(
            display,
            BLACK,
            self.rect,
            border_radius=self.corner_radius,
            border_top_left_radius=self.top_left_corner_radius,
            border_top_right_radius=self.top_right_corner_radius,
            border_bottom_left_radius=self.bottom_left_corner_radius,
            border_bottom_right_radius=self.bottom_right_corner_radius,
        )

        #  Draw the background, if requested.
        #  Background colour is created by taking a fifth of the red, green, blue components of the Base colour.

        if self.background_flag is True:
            pygame.draw.rect(
                display,
                layout_config.muted_colour,
                self.rect,
                border_radius=self.corner_radius,
                border_top_left_radius=self.top_left_corner_radius,
                border_top_right_radius=self.top_right_corner_radius,
                border_bottom_left_radius=self.bottom_left_corner_radius,
                border_bottom_right_radius=self.bottom_right_corner_radius,
            )

        #  Draw the frame, if requested.

        if self.frame_flag == True:
            pygame.draw.rect(
                display,
                self.colour,
                self.rect,
                1,
                border_radius=self.corner_radius,
                border_top_left_radius=self.top_left_corner_radius,
                border_top_right_radius=self.top_right_corner_radius,
                border_bottom_left_radius=self.bottom_left_corner_radius,
                border_bottom_right_radius=self.bottom_right_corner_radius,
            )

        #  Draw the information bar, if requested.

        if self.bar is True:
            pygame.draw.rect(
                display,
                self.colour,
                (self.rect[0], self.rect[1], self.rect[2], 30),
                border_top_left_radius=self.top_left_corner_radius,
                border_top_right_radius=self.top_right_corner_radius,
            )

    def base_to_display_rect(
        self, rect: tuple[int, int, int, int]
    ) -> tuple[int, int, int, int]:
        """base_to_display_rect

        Converts a rectangle in local coordinates to one in absolute display coordinates.

        Args:
            rect (tuple[int, int, int, int]): the rectangle in local cooridnates.

        Returns:
            tuple[int, int, int, int]: the rectangle in absolute display coordinates.
        """
        return (
            self.rect[0] + rect[0],
            self.rect[1] + rect[1],
            rect[2],
            rect[3],
        )
