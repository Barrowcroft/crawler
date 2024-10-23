#  Represents the crawler's life support.

from typing import Any

from crawler.crawler.modules.hold import Hold
from crawler.crawler.modules.module import Module
from crawler.crawler.modules.personnel import Personnel


class LifeSupport(Module):
    """LifeSupport

    Represents the crawler's life support.

    Args:
        Module: The LifeSupport subclasses the Module class.
    """

    def update(self, mitigations: list[tuple[str, str]]) -> None:

        super().update(mitigations)

        if self.status != "ONLINE":
            for _person in self.supported_personnel:
                mitigations = []
                _person.damage(1, mitigations)

    def damage(self, damage_amount: int, mitigations: list[tuple[str, str]]) -> None:
        #  Receives an instruction to apply damage.
        #  Personnel receive heat damage, but there are mitigations.
        #  However, if the life-support is not online then mitigations wont apply.
        #  ie, a medic will keep personnel health at 25%,
        #  but if life-support totally fails offline there is nothing they can do.

        super().damage(damage_amount, mitigations)

        for _person in self.supported_personnel:
            _person.damage(damage_amount, mitigations)

    def __init__(self, hold: Hold, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

        #  Link the supported personnel to the personnel in the hold.
        self.supported_personnel: list[Personnel] = hold.personnel_slots
