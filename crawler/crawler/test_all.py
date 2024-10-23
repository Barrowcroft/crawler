#  POWER TESTING !!!

from crawler.crawler.modules.heat_sink import HeatSink
from crawler.crawler.modules.module import Module
from crawler.crawler.modules.oxygen_source import OxygenSource
from crawler.crawler.modules.power_source import PowerSource


def create_test_modules(
    oxygen_supply: OxygenSource, power_supply: PowerSource, heat_sink: HeatSink
) -> list[Module]:

    _optional_modules: list[Module] = []

    _optional_modules.append(
        Module(
            name="Oxygen Drain",
            description="Drain crawler's oxygen",
            max_health=100,
            oxygen_supply=oxygen_supply,
            oxygen_withdrawal=1000,
            oxygen_withdrawal_essential=False,
            status="OFFLINE",
            module_index=1,
        )
    )
    _optional_modules.append(
        Module(
            name="Oxygen Boost",
            description="Boost crawler's oxygen",
            max_health=100,
            oxygen_supply=oxygen_supply,
            oxygen_deposit=1000,
            oxygen_deposit_essential=False,
            status="OFFLINE",
            module_index=2,
        )
    )
    _optional_modules.append(
        Module(
            name="Power Drain",
            description="Drain crawler's power",
            max_health=100,
            power_supply=power_supply,
            power_withdrawal=1000,
            power_withdrawal_essential=False,
            status="OFFLINE",
            module_index=3,
        )
    )
    _optional_modules.append(
        Module(
            name="Power Boost",
            description="Boost crawler's power",
            max_health=100,
            power_supply=power_supply,
            power_deposit=1000,
            power_deposit_essential=False,
            status="OFFLINE",
            module_index=4,
        )
    )

    _optional_modules.append(
        Module(
            name="Heat Drain",
            description="Drain crawler's heat",
            max_health=100,
            heat_sink=heat_sink,
            heat_withdrawal=0,
            heat_withdrawal_essential=False,
            status="OFFLINE",
            module_index=5,
            mitigation="Habitiat Technician",
        )
    )
    _optional_modules.append(
        Module(
            name="Heat Boost",
            description="Boost crawler's heat",
            max_health=100,
            heat_sink=heat_sink,
            heat_deposit=1000,
            heat_deposit_essential=False,
            status="OFFLINE",
            module_index=6,
        )
    )
    return _optional_modules
