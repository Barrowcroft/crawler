#  Represents the personnel in the crawler's hold.

import crawler.constants as c
from crawler.crawler.modules.reporting.log import module_logger


class Personnel:
    """Personnel

    Represents the personnel in the crawler's hold.
    """

    @property
    def health(self) -> int:
        #  Returns the health level as a percetage of the maximum.
        return int((self.actual_health / self.max_health) * 100)

    @health.setter
    def health(self, value: int) -> None:
        #  Set the health level as a percentage of the maximum.
        self.actual_health = int((self.max_health / 100) * value)

    @property
    def health_level(self) -> int:
        #  Returns the health level. 3 = Danger, 2 = Warning, 1 = Notice, 0 = Normal.
        if self.health <= 25:
            return 3
        elif self.health <= 50:
            return 2
        elif self.health <= 75:
            return 1
        else:
            return 0

    def damage(self, damage_amount: int, mitigations: list[tuple[str, str]]) -> None:
        #  Receives an instruction to apply damage.
        #  If the health drops below 25% and there is a mitigating value then the health is fixed at 25%.
        #  Mitigations are tuples of role and name e.g ("Medic", "John Smith")
        #  If the health falls to zero the person is flagged as being deceased.

        if damage_amount > 0:
            self.actual_health -= damage_amount

            #  Search for a mitigation.

            _index_of_mitigation = next(
                (
                    _index
                    for _index, _mitigation in enumerate(mitigations)
                    if self.mitigation in _mitigation
                ),
                -1,
            )

            #  See if health is being limited by mitigation.

            if self.health < 25 and _index_of_mitigation != -1:
                _mitigation: tuple[str, str] = mitigations[_index_of_mitigation]
                self.health = 25
                if self.name != _mitigation[0]:
                    _message: str = (
                        f"{self.name} is being stablised at 25% health by {_mitigation[1]}, {_mitigation[0]}."
                    )
                else:
                    _message: str = (
                        f"{self.name} is working hard to stay alive and functional."
                    )

                module_logger.log(
                    self.location_name,
                    _message,
                    self.health,
                    self.health_level,
                )

            if self.actual_health <= 0:
                self.actual_health = 0
                self.status = c.PERSONNEL_STATUS_DECEASED
                module_logger.log(
                    self.location_name,
                    f"{self.name}, {self.role}, is deceased.",
                    self.health,
                    self.health_level,
                )

        module_logger.log(
            self.location_name,
            module_logger.messages[self.location_name][0],
            self.health,
            self.health_level,
        )

    def __init__(
        self,
        name: str,
        index: int,
        role: str,
        max_health: int,
        actual_health: int,
        mitigation: str,
    ) -> None:

        self.name: str = name
        self.role: str = role
        self.mitigation = mitigation

        self.max_health: int = max_health
        self.actual_health: int = actual_health

        self.status: str = c.PERSONNEL_STATUS_OK

        self.location_name: str = f"Personnel {str(index)}"

        module_logger.log(
            self.location_name,
            f"{self.name} has been installed in life-support.",
            self.health,
            self.health_level,
        )
