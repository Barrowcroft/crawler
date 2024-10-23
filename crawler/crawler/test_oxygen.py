#  OXYGEN TESTING !!!

from crawler.crawler.modules.module import Module
from crawler.crawler.modules.oxygen_source import OxygenSource


def create_oxygen_test_modules(oxygen_supply: OxygenSource) -> list[Module]:

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
        )
    )
    _optional_modules.append(
        Module(
            name="Oxygen Consumer",
            description="Consume oxygen",
            max_health=100,
            oxygen_supply=oxygen_supply,
            oxygen_withdrawal=10,
            oxygen_withdrawal_essential=False,
            status="OFFLINE",
        )
    )
    _optional_modules.append(
        Module(
            name="Oxygen Consumer",
            description="Consume oxygen - essential",
            max_health=100,
            oxygen_supply=oxygen_supply,
            oxygen_withdrawal=10,
            oxygen_withdrawal_essential=True,
            status="OFFLINE",
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
        )
    )
    _optional_modules.append(
        Module(
            name="Oxygen Creator",
            description="Create oxygen",
            max_health=100,
            oxygen_supply=oxygen_supply,
            oxygen_deposit=100,
            oxygen_deposit_essential=False,
            status="OFFLINE",
        )
    )
    _optional_modules.append(
        Module(
            name="Oxygen Creator",
            description="Create oxygen - essential",
            max_health=100,
            oxygen_supply=oxygen_supply,
            oxygen_deposit=100,
            oxygen_deposit_essential=True,
            status="OFFLINE",
        )
    )

    return _optional_modules
