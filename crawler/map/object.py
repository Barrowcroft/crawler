#  The Object class.
#  Represents objects on the map which may, or may not, have corresponding images.

from typing import Any, Optional

import pygame
import pytmx  # type: ignore


class Object(pygame.sprite.Sprite):
    """Object

    The Object class.

    Args:
        pygame.sprite.Sprite: the Object subclasses pygame.sprite.Sprite.
    """

    def __init__(self, groups: pygame.sprite.Group, rect: pygame.rect.Rect, image: Optional[pygame.Surface], properties: dict[str, Any]) -> None:  # type: ignore
        """__init__

        Initialise the Object.

        Args:
            groups (pygame.sprite.Group): the sprite groups to which the Object belongs.
            rect (pygame.rect.Rect): the objects rectangle.
            image (Optional[pygame.Surface]): the, optional, Object image.
            properties (dict[str, Any]): the properties belonging to the Object, passed from the map.
        """
        super().__init__(groups)  # type: ignore

        self.name: str = "object"
        self.rect: pygame.rect.Rect = rect
        self.image: Optional[pygame.Surface] = image
