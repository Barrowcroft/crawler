#  Represents the crawler's power supply.

from typing import Any

from crawler.crawler.modules.module import Module


class PowerSource(Module):
    """PowerSource

    Represents the crawler's power supply.

    Args:
        Module: The PowerSource subclasses the Module class.
    """

    @property
    def power(self) -> int:
        #  Returns the power level as a percetage of the maximum.
        return int((self.actual_power / self.max_power) * 100)

    @power.setter
    def power(self, value: int) -> None:
        #  Set the power level as a percentage of the maximum.
        self.actual_power = int((self.max_power / 100) * value)

    @property
    def level(self) -> int:
        #  Returns the power warning level. 3 = Danger, 2 = Warning, 1 = Notice, 0 = Normal.
        if self.power <= 25:
            return 3
        elif self.power <= 50:
            return 2
        elif self.power <= 75:
            return 1
        else:
            return 0

    def limit(self) -> None:
        #  Keep actual value between 0 and max.
        self.actual_power = 0 if self.actual_power < 0 else self.actual_power
        self.actual_power = (
            self.max_power if self.actual_power > self.max_power else self.actual_power
        )

    def withdraw(self, amount: int) -> bool:
        #  Receives a request to withdraw power.
        #  If the request is successful, ie the full amount is withdrawn, the method returns True.

        if self.actual_power >= amount:
            _success: bool = True
        else:
            _success = False

        self.actual_power -= amount
        self.limit()

        return _success

    def deposit(self, amount: int) -> bool:
        #  Receives a request to deposit power.
        #  If the deposit is successful, ie the full amount is deposited, so the method returns True.

        if (self.max_power - self.actual_power) >= amount:
            _success: bool = True
        else:
            _success = False

        self.actual_power += amount
        self.limit()

        return _success

    def __init__(self, max_power: int, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

        self.max_power: int = max_power
        self.actual_power: int = max_power
