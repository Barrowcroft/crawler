#  Represents the crawler's hold.

from typing import Any

from crawler.crawler.modules.module import Module
from crawler.crawler.modules.personnel import Personnel
from crawler.crawler.modules.reporting.log import module_logger
from crawler.crawler.modules.salvage import Salvage


class Hold(Module):
    """Hold

    Represents the crawler's hold.

    Args:
        Module: The Hold subclasses the Module class.
    """

    @property
    def number_of_salvage_slots(self) -> int:
        #  Returns the number of available salvage slots.
        #  The number of available slots is determined by the health.
        #  Health of 75% provides 7 slots, 65% provides 6 slots, and so on.
        if self.health == 0:
            return 0
        else:
            return int(self.health / 10)

    def damage(self, damage_amount: int, mitigations: list[tuple[str, str]]) -> None:
        #  Receives an instruction to apply damage.
        #  If the health falls the number of available slots will fall and items in the hold will be destroyed.
        super().damage(damage_amount, mitigations)

        for _index, _salvage in enumerate(
            self.salvage_slots[self.number_of_salvage_slots :]
        ):
            module_logger.log(
                _salvage.name,
                f"{_salvage.name} in hold slot {_index+1} has been destroyed.",
                self.health,
                self.health_level,
            )
            _salvage.destroy()

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

        self.salvage_slots: list[Salvage] = []
        self.personnel_slots: list[Personnel] = []
