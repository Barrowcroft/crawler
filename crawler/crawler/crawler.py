#  The crawler.py file describes the Crawler class.

import os

import pygame

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.crawler.system import System


class Crawler(pygame.sprite.Sprite):
    """Crawler

    The crawler.py file describes the crawler class.
    """

    @property
    def position(self) -> pygame.Vector2:
        """position

        Returns:
            Vector2: position of crawler.
        """
        return self._pos

    @position.setter
    def position(self, value: tuple[int, int]) -> None:
        """position

        Args:
            value (tuple[int, int]): position of crawler.
        """
        self._pos.x = value[0] + (c.MAP_TILE_SIZE / 2)
        self._pos.y = value[1] + (c.MAP_TILE_SIZE / 2)

    def __init__(self, number: int) -> None:  # type: ignore
        """__init__

        Initialise the Crawler.
        """

        customlogger.log_message(
            f"Initialising CRWLR{number+1:02}.",
            customlogger.Levels.INFO,
        )

        super().__init__()  # type: ignore

        #  Initialise the Crawler.

        self.timer: float = 0
        self.active: bool = False
        self.number: int = number
        self.identifier: str = f"CRWLR{number+1:02}"
        position: tuple[int, int] = (0, 0)

        #  Initialise the crawler systems.

        self.system: System = System()

        customlogger.log_message(
            f"Initialised {self.identifier}.",
            customlogger.Levels.INFO,
        )

        #  Load the crawler animation frames

        self._frames: list[pygame.Surface] = []
        self.loadFrames()

        self._ImageIndexModfier: int = 0
        self._imageIndex: int = 0
        self.crawlerImage: pygame.Surface = self._frames[self._imageIndex]

        self.name: str = "crawler"
        self.image: pygame.Surface = self.crawlerImage
        self.rect: pygame.Rect = self.image.get_rect()

        #  Initialise movement variables

        self._rot: int = 0
        self._rot_speed: float = 0

        self._x_pos: int = position[0]
        self._y_pos: int = position[1]
        self._vel: pygame.Vector2 = pygame.Vector2(0, 0)
        self._pos: pygame.Vector2 = pygame.Vector2(
            (self._x_pos * c.MAP_TILE_SIZE) - (c.MAP_TILE_SIZE / 2),  #  type: ignore
            (self._y_pos * c.MAP_TILE_SIZE) - (c.MAP_TILE_SIZE / 2),  #  type: ignore
        )

        self._is_moving: bool = False
        self._is_reversing: bool = False
        self._is_blocked: bool = False

    def handleKeyEvent(self, event: pygame.event.Event) -> None:
        """handleKeyEvent

        Handles keyboard events.
        Up arrow moves forward, down arrow moves back.
        If moving foreward down arrow stops.
        If moving backward up arrow stops.
        Left and right arrows rotate.

        Args:
            event (Event): keyboard event
        """

        self._rot_speed = 0

        if event.type == pygame.KEYDOWN:
            _keys = pygame.key.get_pressed()
            if _keys[pygame.K_UP] and not (
                _keys[pygame.K_LCTRL]
                or _keys[pygame.K_RCTRL]
                or _keys[pygame.K_RALT]
                or _keys[pygame.K_LALT]
            ):
                if self._is_reversing:
                    self._is_moving = False
                    self.system.engine.moving = False
                else:
                    self._is_moving = True
                    self.system.engine.moving = True
                self._is_reversing = False
                self.system.engine.reversing = False
                self._vel = self.adjustVelocity()
                self._active_hit = False
            elif _keys[pygame.K_DOWN] and not (
                _keys[pygame.K_LCTRL]
                or _keys[pygame.K_RCTRL]
                or _keys[pygame.K_RALT]
                or _keys[pygame.K_LALT]
            ):
                if not self._is_reversing:
                    if self._is_moving:
                        self._is_moving = False
                        self._is_reversing = False
                        self.system.engine.moving = False
                        self.system.engine.reversing = False
                    else:
                        self._is_moving = True
                        self._is_reversing = True
                        self.system.engine.moving = True
                        self.system.engine.reversing = True
                else:
                    self._is_moving = True
                    self._is_reversing = True
                    self.system.engine.moving = True
                    self.system.engine.reversing = True
                self._vel = self.adjustVelocity()
                self._active_hit = False
            elif _keys[pygame.K_LEFT]:
                self._rot_speed = c.CRAWLER_ROTATION_SPEED
                self._vel = self.adjustVelocity()
                self._vel = self._vel * 0.2
            elif _keys[pygame.K_RIGHT]:
                self._rot_speed = -c.CRAWLER_ROTATION_SPEED
                self._vel = self.adjustVelocity()
                self._vel = self._vel * 0.2

            self._vel += self._vel * -0.12

    def update(self, dt: float) -> None:
        """update

        Updates the Crawler class.

        Args:
            dt (float): delta time.
        """

        self.adjustSpritePostion(dt)
        self.setNextFrame()

        self.timer += dt
        if self.timer > 0.25:

            self.system.update()

            self.timer = 0

    def stop(self) -> None:
        self._is_moving = False
        self._is_reversing = False

    def adjustVelocity(self) -> pygame.Vector2:
        """ "adjustVelocity

        Adjust the velocity of the crawler.

        """

        if not self._is_moving:
            return pygame.Vector2(0, 0)
        if self._is_reversing:
            return pygame.Vector2(-self.system.engine.speed, 0).rotate(-self._rot)
        else:
            return pygame.Vector2(self.system.engine.speed, 0).rotate(-self._rot)

    def adjustSpritePostion(self, dt: float) -> None:
        """adjustSpritePostion

        Adjusts the position of the sprite to account for collisions or
        map boundaries.

        Args:
            dt (float): deltatime
        """

        self._rot = int((self._rot + (self._rot_speed * dt)) % 360)
        self.image = pygame.transform.rotate(self.crawlerImage, self._rot)
        self.rect = self.image.get_rect()
        self.rect.center = (int(self._pos[0]), int(self._pos[1]))

        self._vel = self.adjustVelocity()
        self._pos += self._vel * dt

        self._pos.x = max(self._pos.x, c.MAP_TILE_SIZE / 2)
        self._pos.y = max(self._pos.y, c.MAP_TILE_SIZE / 2)

        self._pos.x = min(
            self._pos.x,
            (c.MAP_TILES_ACROSS * c.MAP_TILE_SIZE) - (c.MAP_TILE_SIZE / 2) - 3,
        )
        self._pos.y = min(
            self._pos.y,
            (c.MAP_TILES_DOWN * c.MAP_TILE_SIZE) - c.MAP_TILE_SIZE - 30,
        )

    def loadFrames(self) -> None:
        """loadFrames

        Loads the crawler animation frames

        """

        self._frames = []
        for _index in range(0, c.CRAWLER_FRAME_COUNT):
            self._frames.append(
                pygame.image.load(
                    os.path.join(
                        "crawler",
                        c.DIR_ASSETS,
                        c.DIR_CRAWLER,
                        f"{c.DIR_CRAWLER}{self.number+1}",
                        f"{c.CRAWLER_ANIMATION_FILENAME}_{self.number+1}_{_index:02}.png",
                    )
                )
            )

    def setNextFrame(self) -> None:
        """setNextFrame

        Sets the next crawler animation frame.

        """

        if self._vel.x != 0 or self._vel.y != 0:
            if self.system.engine.reversing is False:
                self._ImageIndexModfier = (self._ImageIndexModfier - 1) % 10
                if self._ImageIndexModfier == 0:
                    self._imageIndex = (self._imageIndex - 1) % 10
            else:
                self._ImageIndexModfier = (self._ImageIndexModfier + 1) % 10
                if self._ImageIndexModfier == 0:
                    self._imageIndex = (self._imageIndex + 1) % 10
            self.crawlerImage = self._frames[self._imageIndex]
