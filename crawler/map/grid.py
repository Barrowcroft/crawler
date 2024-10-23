#  The Grid class.
#  The Grid is drawn over the map and other sprites.

import pygame


class Grid(pygame.sprite.Sprite):
    """Grid

    The Grid class.

    Args:
        pygame.sprite.Sprite: the Grid subclasses pygame.sprite.Sprite.
    """

    def __init__(self, group: pygame.sprite.Group, grid: pygame.Surface) -> None:  # type: ignore
        """__init__

        Initialise the Grid.

        Args:
            group (pygame.sprite.Group): the sprite groups to which the Grid belongs.
            grid (pygame.Surface): the surface containing the Grid image.
        """
        super().__init__(group)  # type: ignore

        self.name: str = "grid"
        self.image: pygame.Surface = grid
        self.rect: pygame.rect.Rect = grid.get_rect()  # type: ignore
