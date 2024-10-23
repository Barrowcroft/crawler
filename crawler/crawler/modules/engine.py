#  Represents the crawler's engine.

from typing import Any

from crawler.crawler.modules.module import Module


class Engine(Module):
    """Engine

    Represents the crawler's engine.

    Args:
        Module: The Engine subclasses the Module class.
    """

    @property
    def actual_heat_deposit(self) -> int:
        #  Returns the actual heat deposit.
        return self.heat_deposit * self.terrain

    @property
    def revs(self) -> int:
        #  Returns the revs as a percetage.

        if self.moving is False:
            return 25

        if self.terrain == 3:
            return 100
        elif self.terrain == 2:
            return 75
        elif self.terrain == 1:
            return 50
        else:
            return 25

    @property
    def revs_level(self) -> int:
        #  Returns the revs level.

        if self.moving is False:
            return 0

        if self.terrain == 3:
            return 3
        elif self.terrain == 2:
            return 2
        elif self.terrain == 1:
            return 1
        else:
            return 0

    @property
    def speed(self) -> int:
        #  Returns the speed as a percetage.

        if self.moving is False:
            return 0

        _speed: int = 0

        if self.terrain == 3:
            _speed = 25
        elif self.terrain == 2:
            _speed = 50
        elif self.terrain == 1:
            _speed = 75
        else:
            _speed = 100

        if self.reversing is True:
            _speed = int(_speed / 2)

        return _speed

    @property
    def speed_level(self) -> int:
        #  Returns the speed level.

        if self.moving is False:
            return 0

        if self.terrain == 3:
            return 3
        elif self.terrain == 2:
            return 2
        elif self.terrain == 1:
            return 1
        else:
            return 0

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

        self.terrain: int = 0
        self.moving: bool = False
        self.reversing: bool = False
