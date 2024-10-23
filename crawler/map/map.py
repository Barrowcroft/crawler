#  The Map class.

import pygame


class Map(pygame.sprite.Sprite):
    """Map

    The Map class.

    Args:
        pygame.sprite.Sprite: the Map subclasses pygame.sprite.Sprite.
    """

    def __init__(self, group: pygame.sprite.Group, map: pygame.Surface) -> None:  # type: ignore
        """__init__

        Initialise the Map.

        Args:
            groups (pygame.sprite.Group): the sprite groups to which the Map belongs.
            map (pygame.Surface): the surface containing the Map image.
        """
        super().__init__(group)  # type: ignore

        self.name: str = "map"
        self.image: pygame.Surface = map
        self.rect: pygame.rect.Rect = map.get_rect()  # type: ignore
