#  HEAT TESTING !!!

from crawler.crawler.modules.heat_sink import HeatSink
from crawler.crawler.modules.module import Module


def create_heat_test_modules(heat_sink: HeatSink) -> list[Module]:

    _optional_modules: list[Module] = []
    _optional_modules.append(
        Module(
            name="Heat Drain",
            description="Drain crawler's heat",
            max_health=100,
            heat_sink=heat_sink,
            heat_withdrawal=0,
            heat_withdrawal_essential=False,
            status="OFFLINE",
            module_index=1,
            mitigation="Habitiat Technician",
        )
    )
    _optional_modules.append(
        Module(
            name="Heat Consumer",
            description="Consume heat",
            max_health=100,
            heat_sink=heat_sink,
            heat_withdrawal=10,
            heat_withdrawal_essential=False,
            status="OFFLINE",
            module_index=2,
        )
    )
    _optional_modules.append(
        Module(
            name="Heat Consumer",
            description="Consume heat - essential",
            max_health=100,
            heat_sink=heat_sink,
            heat_withdrawal=10,
            heat_withdrawal_essential=True,
            status="OFFLINE",
            module_index=3,
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
            module_index=4,
        )
    )
    _optional_modules.append(
        Module(
            name="Heat Creator",
            description="Create heat",
            max_health=100,
            heat_sink=heat_sink,
            heat_deposit=10,
            heat_deposit_essential=False,
            status="OFFLINE",
            module_index=5,
        )
    )
    _optional_modules.append(
        Module(
            name="Heat Creator",
            description="Create heat - essential",
            max_health=100,
            heat_sink=heat_sink,
            heat_deposit=10,
            heat_deposit_essential=True,
            status="OFFLINE",
            module_index=6,
        )
    )

    return _optional_modules
