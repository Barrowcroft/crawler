#  Represents the crawler's heat sink.

from typing import Any

from crawler.crawler.modules.module import Module


class HeatSink(Module):
    """HeatSink

    Represents the crawler's heat sink.

    Args:
        Module: The HeatSink subclasses the Module class.
    """

    @property
    def heat(self) -> int:
        #  Returns the heat level as a percetage of the maximum.
        return int((self.actual_heat / self.max_heat) * 100)

    @heat.setter
    def heat(self, value: int) -> None:
        #  Set the heat level as a percentage of the maximum.
        self.actual_heat = int((self.max_heat / 100) * value)

    @property
    def level(self) -> int:
        #  Returns the heat warning level. 3 = Danger, 2 = Warning, 1 = Notice, 0 = Normal.
        if self.heat <= 25:
            return 0
        elif self.heat <= 50:
            return 1
        elif self.heat <= 75:
            return 2
        else:
            return 3

    def limit(self) -> None:
        self.heat = 20 if self.heat < 20 else self.heat
        self.heat = 100 if self.heat > 100 else self.heat

    def withdraw(self, amount: int) -> bool:
        #  Receives a request to withdraw heat.
        #  If the request is successful the method returns True.

        if self.actual_heat >= amount:
            _success: bool = True
        else:
            _success = False

        self.actual_heat -= amount
        self.limit()
        return _success

    def deposit(self, amount: int) -> bool:
        #  Receives a request to deposit heat.
        #  Heat can only be deposited if the heat is below 85%.
        #  If the request is successful the method returns True.

        if self.heat <= 85:
            self.actual_heat += amount
            self.limit()
            return True
        return False

    def update(self, mitigations: list[tuple[str, str]]) -> None:
        self.limit()
        if self.heat > 80:
            for _module in self.damagable_modules:
                _module.damage(
                    self.damage_amount,
                    mitigations,
                )

    def __init__(
        self, max_heat: int, damage_amount: int, *args: Any, **kwargs: Any
    ) -> None:

        super().__init__(*args, **kwargs)

        self.max_heat: int = max_heat
        self.actual_heat: int = 20

        self.damagable_modules: list[Module] = []
        self.damage_amount: int = damage_amount
