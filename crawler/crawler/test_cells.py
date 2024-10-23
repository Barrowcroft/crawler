#  POWER TESTING !!!

from crawler.crawler.modules.module import Module
from crawler.crawler.modules.power_source import PowerSource


def create_cells_test_modules(power_supply: PowerSource) -> list[Module]:

    _optional_modules: list[Module] = []
    _optional_modules.append(
        Module(
            name="Power Drain",
            description="Drain crawler's power",
            max_health=100,
            power_supply=power_supply,
            power_withdrawal=1000,
            power_withdrawal_essential=False,
            status="OFFLINE",
            module_index=1,
        )
    )
    _optional_modules.append(
        Module(
            name="Power Consumer",
            description="Consume power",
            max_health=100,
            power_supply=power_supply,
            power_withdrawal=10,
            power_withdrawal_essential=False,
            status="OFFLINE",
            module_index=2,
        )
    )
    _optional_modules.append(
        Module(
            name="Power Consumer",
            description="Consume power - essential",
            max_health=100,
            power_supply=power_supply,
            power_withdrawal=10,
            power_withdrawal_essential=True,
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
            name="Power Creator",
            description="Create power",
            max_health=100,
            power_supply=power_supply,
            power_deposit=100,
            power_deposit_essential=False,
            status="OFFLINE",
            module_index=5,
        )
    )
    _optional_modules.append(
        Module(
            name="Power Creator",
            description="Create power - essential",
            max_health=100,
            power_supply=power_supply,
            power_deposit=100,
            power_deposit_essential=True,
            status="OFFLINE",
            module_index=6,
        )
    )

    return _optional_modules
