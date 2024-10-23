#  Represents the crawler;s oxygen supply.

from typing import Any

from crawler.crawler.modules.module import Module


class OxygenSource(Module):
    """OxygenSource

    Represents the crawler;s oxygen supply.

    Args:
        Module: The OxygenSource subclasses the Module class.
    """

    @property
    def oxygen(self) -> int:
        #  Returns the oxygen level as a percetage of the maximum.
        return int((self.actual_oxygen / self.max_oxygen) * 100)

    @oxygen.setter
    def oxygen(self, value: int) -> None:
        #  Set the oxygen level as a percentage of the maximum.
        self.actual_oxygen = int((self.max_oxygen / 100) * value)

    @property
    def level(self) -> int:
        #  Returns the oxygen warning level. 3 = Danger, 2 = Warning, 1 = Notice, 0 = Normal.
        if self.oxygen <= 25:
            return 3
        elif self.oxygen <= 50:
            return 2
        elif self.oxygen <= 75:
            return 1
        else:
            return 0

    def limit(self) -> None:
        #  Keep actual value between 0 and max.
        self.actual_oxygen = 0 if self.actual_oxygen < 0 else self.actual_oxygen
        self.actual_oxygen = (
            self.max_oxygen
            if self.actual_oxygen > self.max_oxygen
            else self.actual_oxygen
        )

    def withdraw(self, amount: int) -> bool:
        #  Receives a request to withdraw oxygen.
        #  If the request is successful, ie the full amount is withdrawn, the method returns True.

        if self.actual_oxygen >= amount:
            _success: bool = True
        else:
            _success = False

        self.actual_oxygen -= amount
        self.limit()

        return _success

    def deposit(self, amount: int) -> bool:
        #  Receives a request to deposit oxygen.
        #  If the deposit is successful, ie the full amount is deposited, so the method returns True.

        if (self.max_oxygen - self.actual_oxygen) >= amount:
            _success: bool = True
        else:
            _success = False

        self.actual_oxygen += amount
        self.limit()

        return _success

    def __init__(self, max_oxygen: int, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

        self.information: str = ""

        self.max_oxygen: int = max_oxygen
        self.actual_oxygen: int = max_oxygen
