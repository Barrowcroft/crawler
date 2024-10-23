#  Represents the module object.

from typing import Optional, Protocol

import crawler.constants as c
from crawler.crawler.modules.reporting.log import module_logger


class OxygenSource(Protocol):

    @property
    def oxygen(self) -> int:  # type:ignore
        #  Returns the oxygen level as a percetage of the maximum.
        pass

    @oxygen.setter
    def oxygen(self, value: int) -> None:
        #  Set the oxygen level as a percentage of the maximum.
        pass

    def withdraw(self, amount: int) -> bool:  # type:ignore
        #  Receives a request to withdraw oxygen.
        #  If the request is successful the method returns True.
        pass

    def deposit(self, amount: int) -> bool:  # type:ignore
        #  Receives a request to deposit oxygen.
        #  Deposit requests are always successful so the method returns True.
        pass


class PowerSource(Protocol):

    @property
    def power(self) -> int:  # type:ignore
        #  Returns the power level as a percetage of the maximum.
        pass

    @power.setter
    def power(self, value: int) -> None:
        #  Set the power level as a percentage of the maximum.
        pass

    def withdraw(self, amount: int) -> bool:  # type:ignore
        #  Receives a request to withdraw power.
        #  If the request is successful the method returns True.
        pass

    def deposit(self, amount: int) -> bool:  # type:ignore
        #  Receives a request to deposit power.
        #  Deposit requests are always successful so the method returns True.
        pass


class HeatSink(Protocol):

    @property
    def heat(self) -> int:  # type:ignore
        #  Returns the heat level as a percetage of the maximum.
        pass

    @heat.setter
    def heat(self, value: int) -> None:
        #  Set the heat level as a percentage of the maximum.
        pass

    def withdraw(self, amount: int) -> bool:  # type:ignore
        #  Receives a request to withdraw heat.
        #  If the request is successful the method returns True.
        pass

    def deposit(self, amount: int) -> bool:  # type:ignore
        #  Receives a request to deposit heat.
        #  Deposit requests are always successful so the method returns True.
        pass


class Module:
    """Module

    Represents the module object.
    """

    @property
    def actual_heat_deposit(self) -> int:
        #  Returns the actual heat deposit.
        return self.heat_deposit

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

    def toggle_online(self) -> None:
        #  Toggles the module online / offline.
        if self.status == "ONLINE":
            self.status = c.MODULE_STATUS_OFFLINE_BY_REQUEST
            module_logger.log(
                self.module_name,
                f"{self.name} has been manually taken offline.",
                self.health,
                self.health_level,
            )
        elif self.status.startswith("OFFLINE"):
            self.status = "ONLINE"
            module_logger.log(
                self.module_name,
                f"{self.name} has been manually taken online.",
                self.health,
                self.health_level,
            )

    def update(self, mitigations: list[tuple[str, str]]) -> None:

        #  Store the mitigations for later checking.

        self.mitigations = mitigations

        #  All modules can withdraw or deposit, oxygen, power or heat.
        #  Not all modules will do all three; in which case the amount will be zero.

        self.update_oxygen()
        self.update_power()
        self.update_heat()

    def update_oxygen(self) -> None:

        if self.oxygen_supply is None:
            return

        #  If still online, or offline to due to oxygen deficiency, request to withdraw oxygen from oxygen supply.
        #  If oxygen withdrawal is essential and the full amount of oxygen is not withdrawn
        #  then the module goes off line due to lack of oxygen.
        #  It is unlikely that any module will both withdraw and deposit oxygen.
        if (
            self.status == c.MODULE_STATUS_ONLINE
            or self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_OXYGEN_DEFICIENCY
        ):
            _oxygen_withdrawn: bool = self.oxygen_supply.withdraw(
                self.oxygen_withdrawal
            )

            #  If oxygen deficiency go offline.
            if (
                self.oxygen_withdrawal_essential
                and _oxygen_withdrawn is not True
                and self.status != c.MODULE_STATUS_OFFLINE_DUE_TO_OXYGEN_DEFICIENCY
            ):
                self.status = c.MODULE_STATUS_OFFLINE_DUE_TO_OXYGEN_DEFICIENCY
                module_logger.log(
                    self.module_name,
                    f"{self.name} has gone offline due to oxygen deficiency.",
                    self.health,
                    self.health_level,
                )
                return

            #  If oxygen is restored go back online.
            if (
                _oxygen_withdrawn is True
                and self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_OXYGEN_DEFICIENCY
            ):
                self.status = "ONLINE"
                module_logger.log(
                    self.module_name,
                    f"{self.name} has gone online due to restored oxygen.",
                    self.health,
                    self.health_level,
                )
                return

        #  If still online, request to deposit oxygen to oxygen supply.
        #  It is unlikely that any module will both withdraw and deposit oxygen.

        if (
            self.status == c.MODULE_STATUS_ONLINE
            or self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_OXYGEN_EXCESS
        ):
            _oxygen_deposited: bool = self.oxygen_supply.deposit(self.oxygen_deposit)

            #  If oxygen excess go offline.

            if (
                self.oxygen_deposit_essential
                and _oxygen_deposited is not True
                and self.status != c.MODULE_STATUS_OFFLINE_DUE_TO_OXYGEN_EXCESS
            ):
                self.status = c.MODULE_STATUS_OFFLINE_DUE_TO_OXYGEN_EXCESS
                module_logger.log(
                    self.module_name,
                    f"{self.name} has gone offline due to oxygen excess.",
                    self.health,
                    self.health_level,
                )
                return

            #  If oxygen is restored go back online.

            if (
                _oxygen_deposited is True
                and self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_OXYGEN_EXCESS
            ):
                self.status = "ONLINE"
                module_logger.log(
                    self.module_name,
                    f"{self.name} has gone online due to reduced oxygen.",
                    self.health,
                    self.health_level,
                )
                return

    def update_power(self) -> None:

        if self.power_supply is None:
            return

        #  If still online, or offline to due to power deficiency, request to withdraw power from power supply.
        #  If power withdrawal is essential and the full amount of power is not withdrawn
        #  then the module goes off line due to lack of power.
        #  It is unlikely that any module will both withdraw and deposit power.
        if (
            self.status == c.MODULE_STATUS_ONLINE
            or self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_POWER_DEFICIENCY
        ):
            _power_withdrawn: bool = self.power_supply.withdraw(self.power_withdrawal)

            #  If power deficiency go offline.
            if (
                self.power_withdrawal_essential
                and _power_withdrawn is not True
                and self.status != c.MODULE_STATUS_OFFLINE_DUE_TO_POWER_DEFICIENCY
            ):
                self.status = c.MODULE_STATUS_OFFLINE_DUE_TO_POWER_DEFICIENCY
                module_logger.log(
                    self.module_name,
                    f"{self.name} has gone offline due to power deficiency.",
                    self.health,
                    self.health_level,
                )
                return

            #  If power is restored go back online.
            if (
                _power_withdrawn is True
                and self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_POWER_DEFICIENCY
            ):
                self.status = "ONLINE"
                module_logger.log(
                    self.module_name,
                    f"{self.name} has gone online due to restored power.",
                    self.health,
                    self.health_level,
                )
                return

        #  If still online, request to deposit power to power supply.
        #  It is unlikely that any module will both withdraw and deposit power.

        if (
            self.status == c.MODULE_STATUS_ONLINE
            or self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_POWER_EXCESS
        ):
            _power_deposited: bool = self.power_supply.deposit(self.power_deposit)

            #  If power excess go offline.

            if (
                self.power_deposit_essential
                and _power_deposited is not True
                and self.status != c.MODULE_STATUS_OFFLINE_DUE_TO_POWER_EXCESS
            ):
                self.status = c.MODULE_STATUS_OFFLINE_DUE_TO_POWER_EXCESS
                module_logger.log(
                    self.module_name,
                    f"{self.name} has gone offline due to power excess.",
                    self.health,
                    self.health_level,
                )
                return

            #  If power is restored go back online.

            if (
                _power_deposited is True
                and self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_POWER_EXCESS
            ):
                self.status = "ONLINE"
                module_logger.log(
                    self.module_name,
                    f"The {self.name} has gone online due to reduced power.",
                    self.health,
                    self.health_level,
                )
                return

    def update_heat(self) -> None:

        if self.heat_sink is None:
            return

        #  If still online, or offline to due to heat deficiency, request to withdraw heat from heat supply.
        #  If heat withdrawal is essential and the full amount of heat is not withdrawn
        #  then the module goes off line due to lack of heat.
        #  It is unlikely that any module will both withdraw and deposit heat.
        if (
            self.status == c.MODULE_STATUS_ONLINE
            or self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_HEAT_DEFICIENCY
        ):
            _heat_withdrawn: bool = self.heat_sink.withdraw(self.heat_withdrawal)

            #  If heat deficiency go offline.
            if (
                self.heat_withdrawal_essential
                and _heat_withdrawn is not True
                and self.status != c.MODULE_STATUS_OFFLINE_DUE_TO_HEAT_DEFICIENCY
            ):
                self.status = c.MODULE_STATUS_OFFLINE_DUE_TO_HEAT_DEFICIENCY
                module_logger.log(
                    self.module_name,
                    f"{self.name} has gone offline due to heat deficiency.",
                    self.health,
                    self.health_level,
                )
                return

            #  If heat is restored go back online.
            if (
                _heat_withdrawn is True
                and self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_HEAT_DEFICIENCY
            ):
                self.status = "ONLINE"
                module_logger.log(
                    self.module_name,
                    f"{self.name} has gone online due to restored heat.",
                    self.health,
                    self.health_level,
                )
                return

        #  If still online, request to deposit heat to heat supply.
        #  It is unlikely that any module will both withdraw and deposit heat.

        if (
            self.status == c.MODULE_STATUS_ONLINE
            or self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_HEAT_EXCESS
        ):

            _heat_deposited: bool = self.heat_sink.deposit(self.actual_heat_deposit)
            #  If heat excess go offline.

            if (
                self.heat_deposit_essential
                and _heat_deposited is not True
                and self.status != c.MODULE_STATUS_OFFLINE_DUE_TO_HEAT_EXCESS
            ):
                self.status = c.MODULE_STATUS_OFFLINE_DUE_TO_HEAT_EXCESS
                module_logger.log(
                    self.module_name,
                    f"{self.name} has gone offline due to heat excess.",
                    self.health,
                    self.health_level,
                )
                return

            #  If heat is restored go back online.

            if (
                _heat_deposited is True
                and self.status == c.MODULE_STATUS_OFFLINE_DUE_TO_HEAT_EXCESS
            ):
                self.status = "ONLINE"
                module_logger.log(
                    self.module_name,
                    f"{self.name} has gone online due to reduced heat.",
                    self.health,
                    self.health_level,
                )
                return

    def damage(self, damage_amount: int, mitigations: list[tuple[str, str]]) -> None:
        #  Applies damage to the module.
        #  If the health drops below 25% and there is a mitigating value then the health is fixed at 25%.
        #  If the health falls to zero the module is flagged as having failed.

        if self.status != c.MODULE_STATUS_ONLINE:
            return

        if damage_amount > 0:
            self.actual_health -= damage_amount
            _mitigation: Optional[tuple[str, str]] = self.get_mitigation(mitigations)
            if self.health < 25 and _mitigation is not None:
                self.health = 25
                module_logger.log(
                    self.module_name,
                    f"{self.name} is stablised at 25% by {_mitigation[1]}, {_mitigation[0]}.",
                    self.health,
                    self.health_level,
                )
            else:
                module_logger.log(
                    self.module_name,
                    f"{self.name} is taking heat damage.",
                    self.health,
                    self.health_level,
                )
            if self.actual_health <= 0:
                self.actual_health = 0
                self.status = c.MODULE_STATUS_FAILED_DUE_TO_HEAT_DAMAGE
                module_logger.log(
                    self.module_name,
                    f"{self.name} has failed due to heat damage.",
                    self.health,
                    self.health_level,
                )

        module_logger.log(
            self.module_name,
            module_logger.messages[self.module_name][0],
            self.health,
            self.health_level,
        )

    def get_mitigation(
        self, mitigations: list[tuple[str, str]]
    ) -> Optional[tuple[str, str]]:
        #  Look to see if there is a mitigation that matches that of the module.
        _index_of_mitigation = next(
            (
                _index
                for _index, _mitigation in enumerate(mitigations)
                if self.mitigation in _mitigation
            ),
            -1,
        )
        #  If there is then return the mmitigation otherwise return None.
        if _index_of_mitigation >= 0:
            return mitigations[_index_of_mitigation]
        else:
            return None

    def __init__(
        self,
        name: str = "Module",
        description: str = "This is a crawler module",
        information: str = "",
        class_level: int = 1,
        status: str = c.MODULE_STATUS_ONLINE,
        mitigation: str = "",
        max_health: int = 1000,
        oxygen_supply: Optional[OxygenSource] = None,
        oxygen_withdrawal: int = 0,
        oxygen_withdrawal_essential: bool = False,
        oxygen_deposit: int = 0,
        oxygen_deposit_essential: bool = False,
        power_supply: Optional[PowerSource] = None,
        power_withdrawal: int = 0,
        power_withdrawal_essential: bool = False,
        power_deposit: int = 0,
        power_deposit_essential: bool = False,
        heat_sink: Optional[HeatSink] = None,
        heat_withdrawal: int = 0,
        heat_withdrawal_essential: bool = False,
        heat_deposit: int = 0,
        heat_deposit_essential: bool = False,
        module_index: int = 0,
    ) -> None:

        self.name: str = name
        self.description: str = description
        self.information: str = information
        self.class_level: int = class_level
        self.status: str = status
        self.mitigation: str = mitigation
        self.max_health: int = max_health
        self.actual_health: int = max_health

        #  Connect to oxygen supply.

        self.oxygen_supply: Optional[OxygenSource] = oxygen_supply
        self.oxygen_withdrawal: int = oxygen_withdrawal
        self.oxygen_withdrawal_essential: bool = oxygen_withdrawal_essential
        self.oxygen_deposit: int = oxygen_deposit
        self.oxygen_deposit_essential: bool = oxygen_deposit_essential

        #  connect to power supply.

        self.power_supply: Optional[PowerSource] = power_supply
        self.power_withdrawal: int = power_withdrawal
        self.power_withdrawal_essential: bool = power_withdrawal_essential
        self.power_deposit: int = power_deposit
        self.power_deposit_essential: bool = power_deposit_essential

        #  connect to heat sink.

        self.heat_sink: Optional[HeatSink] = heat_sink
        self.heat_withdrawal: int = heat_withdrawal
        self.heat_withdrawal_essential: bool = heat_withdrawal_essential
        self.heat_deposit: int = heat_deposit
        self.heat_deposit_essential: bool = heat_deposit_essential

        #  Set name for logger.

        self.module_name: str = self.name
        if module_index != 0:
            self.module_name = f"Module {module_index}"

        if self.status != "ONLINE":
            module_logger.log(
                self.module_name,
                f"{self.name} is offline.",
                self.health,
                self.health_level,
            )
        else:
            module_logger.log(
                self.module_name,
                f"{self.name} is functioning normally.",
                self.health,
                self.health_level,
            )
