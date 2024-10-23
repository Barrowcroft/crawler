#  The ModuleInfo and System classes..

from dataclasses import dataclass, field
from typing import Callable, Optional

from crawler.crawler.modules.cooler import Cooler
from crawler.crawler.modules.engine import Engine
from crawler.crawler.modules.heat_sink import HeatSink
from crawler.crawler.modules.hold import Hold
from crawler.crawler.modules.life_support import LifeSupport
from crawler.crawler.modules.module import Module
from crawler.crawler.modules.oxygen_source import OxygenSource
from crawler.crawler.modules.personnel import Personnel
from crawler.crawler.modules.power_source import PowerSource
from crawler.crawler.modules.reporting.log import module_logger
from crawler.crawler.modules.salvage import Salvage
from crawler.crawler.test_all import create_test_modules
from crawler.crawler.test_cells import create_cells_test_modules
from crawler.crawler.test_heat import create_heat_test_modules
from crawler.crawler.test_oxygen import create_oxygen_test_modules

#  Keep these here until they have been tweaked.
#  Then move to constants file.

MAX_OXYGEN_SUPPLY = 10000
MAX_CELLS_HEALTH = 100
MAX_CELLS_SUPPLY = 10000
MAX_HOLD_HEALTH = 100
MAX_HEAT_SINK_HEAT = 100
HEAT_SINK_DAMAGE = 1
MAX_ENGINE_HEALTH = 100
ENGINE_POWER_WITHDRAWAL = 1
ENGINE_HEAT_DEPOSIT = 1
MAX_COOLER_HEALTH = 100
COOLER_POWER_WITHDRAWAL = 1
COOLER_HEAT_WITHDRAWL = 2
LIFESUPPORT_MAX_HEALTH = 100
LIFESUPPORT_OXYGEN_WITHDRAWAL = 1
LIFESUPPORT_POWER_WITHDRAWAL = 1
LIFESUPPORT_HEAT_DEPOSIT = 1

TEST = "ALL"  # "ALL", "OXYGEN", "POWER", "CELLS"


@dataclass
class ModuleInfo:
    """<oduleInfo

    The module info class holds together all the information about the module
    that is needed to display on the console.
    """

    warning_light_levels: list[int] = field(default_factory=list)

    dial_light_levels: list[int] = field(default_factory=list)
    dial_light_percent: list[int] = field(default_factory=list)

    system_light_levels: list[int] = field(default_factory=list)
    system_light_percent: list[int] = field(default_factory=list)
    system_light_status: list[str] = field(default_factory=list)

    personnel_light_texts: list[tuple[str, str]] = field(default_factory=list)
    personnel_light_levels: list[int] = field(default_factory=list)
    personnel_light_percent: list[int] = field(default_factory=list)
    personnel_light_status: list[str] = field(default_factory=list)

    salvage_light_texts: list[tuple[str, str]] = field(default_factory=list)
    salvage_light_levels: list[int] = field(default_factory=list)
    salvage_light_percent: list[int] = field(default_factory=list)
    salvage_light_status: list[str] = field(default_factory=list)

    optional_module_light_texts: list[tuple[str, str, str]] = field(
        default_factory=list
    )
    optional_module_light_levels: list[int] = field(default_factory=list)
    optional_module_light_percent: list[int] = field(default_factory=list)
    optional_module_light_status: list[str] = field(default_factory=list)
    optional_module_light_actions: list[Optional[Callable[[], None]]] = field(
        default_factory=list
    )


class System:
    """System

    System class.
    """

    def __init__(self) -> None:
        """__init__

        Initialises the crawler's modules.

        """

        #  Initialiase system modules.

        self.oxygen: OxygenSource = OxygenSource(
            name="Oxygen Supply Module",
            description="The crawler's oxygen supply",
            max_oxygen=MAX_OXYGEN_SUPPLY,
            mitigation="Habitat Technician",
        )
        self.heat_sink: HeatSink = HeatSink(
            name="Heat Sink",
            description="The crawler's heat sink",
            max_heat=MAX_HEAT_SINK_HEAT,
            damage_amount=HEAT_SINK_DAMAGE,
            mitigation="Energy Specialist",
        )
        self.cells: PowerSource = PowerSource(
            name="Power Cells Module",
            description="The crawler's power supply",
            information="These are the default power cells for the crawler",
            max_health=MAX_CELLS_HEALTH,
            max_power=MAX_CELLS_SUPPLY,
            mitigation="Energy Specialist",
        )
        self.hold: Hold = Hold(
            name="Hold",
            description="The crawler's hold",
            information="This is the default hold configuration for the crawler",
            max_health=MAX_HOLD_HEALTH,
            mitigation="Structural Engineer",
        )
        self.engine: Engine = Engine(
            name="Engine Module",
            description="The crawler's enigne",
            information="This is the default engine for the crawler",
            max_health=MAX_ENGINE_HEALTH,
            power_supply=self.cells,
            power_withdrawal=ENGINE_POWER_WITHDRAWAL,
            power_withdrawal_essential=True,
            heat_sink=self.heat_sink,
            heat_deposit=ENGINE_HEAT_DEPOSIT,
            heat_deposit_essential=False,
            mitigation="Engineer",
        )
        self.cooler: Cooler = Cooler(
            name="Cooler Module",
            description="The crawler's cooler",
            information="This is the default cooler for the crawler",
            max_health=MAX_COOLER_HEALTH,
            power_supply=self.cells,
            power_withdrawal=COOLER_POWER_WITHDRAWAL,
            power_withdrawal_essential=True,
            heat_sink=self.heat_sink,
            heat_withdrawal=COOLER_HEAT_WITHDRAWL,
            heat_withdrawal_essential=False,
            mitigation="Habitat Technician",
        )
        self.life_support: LifeSupport = LifeSupport(
            name="Life-Support Module",
            description="The crawler's life-support",
            information="This is the default life-support for the crawler",
            hold=self.hold,
            max_health=LIFESUPPORT_MAX_HEALTH,
            oxygen_supply=self.oxygen,
            oxygen_withdrawal=LIFESUPPORT_OXYGEN_WITHDRAWAL,
            oxygen_withdrawal_essential=True,
            power_supply=self.cells,
            power_withdrawal=LIFESUPPORT_POWER_WITHDRAWAL,
            power_withdrawal_essential=True,
            heat_sink=self.heat_sink,
            heat_deposit=LIFESUPPORT_HEAT_DEPOSIT,
            heat_deposit_essential=False,
            mitigation="Habitat Technician",
        )

        for _index in range(10):
            module_logger.log(f"Personnel {str(_index+1)}", "Unused", 0, 0)

        for _index in range(6):
            module_logger.log(f"Module {str(_index+1)}", "Unused", 0, 0)

        #  TEST MODULES

        if TEST == "ALL":  #  type: ignore
            self.optional_modules: list[Module] = create_test_modules(
                self.oxygen, self.cells, self.heat_sink
            )

        if TEST == "OXYGEN":  #  type: ignore
            self.optional_modules: list[Module] = create_oxygen_test_modules(
                self.oxygen
            )

        if TEST == "POWER":  #  type: ignore
            self.optional_modules: list[Module] = create_cells_test_modules(self.cells)

        if TEST == "HEAT":  #  type: ignore
            self.optional_modules: list[Module] = create_heat_test_modules(
                self.heat_sink
            )

        #  TEST PERSONNEL

        self.hold.personnel_slots.append(
            Personnel("Keith White", 1, "Engineer", 100, 76, "Medic")
        )
        self.hold.personnel_slots.append(
            Personnel("Jane WIlson", 2, "Habitat Technician", 100, 45, "Medic")
        )
        self.hold.personnel_slots.append(
            Personnel("Claire Samson", 3, "Medic", 100, 68, "Medic")
        )
        self.hold.personnel_slots.append(
            Personnel("Simon Dupont", 4, "System Specialist", 100, 23, "Medic")
        )

        #  TEST SALVAGE

        self.hold.salvage_slots.append(
            Salvage("Salvaged Item", "Salvaged from the surface", 45)
        )
        self.hold.salvage_slots.append(
            Salvage("Salvaged Item", "Salvaged from the surface", 80)
        )
        self.hold.salvage_slots.append(
            Salvage("Salvaged Item", "Salvaged from the surface", 25)
        )
        self.hold.salvage_slots.append(
            Salvage("Salvaged Item", "Salvaged from the surface", 65)
        )
        self.hold.salvage_slots.append(
            Salvage("Salvaged Item", "Salvaged from the surface", 69)
        )
        self.hold.salvage_slots.append(
            Salvage("Salvaged Item", "Salvaged from the surface", 30)
        )

        #  Add modules to heat sink, so that damage can be applied.

        self.heat_sink.damagable_modules.append(self.cells)
        self.heat_sink.damagable_modules.append(self.hold)
        self.heat_sink.damagable_modules.append(self.engine)
        self.heat_sink.damagable_modules.append(self.cooler)
        self.heat_sink.damagable_modules.append(self.life_support)

        for _index, _module in enumerate(self.optional_modules):
            self.heat_sink.damagable_modules.append(_module)

    def update(self) -> None:
        """update

        Updates all the crawler's modules.
        """

        #  Extract mitigating personnel.

        _mitigations = [
            (_mitigation.name, _mitigation.role)
            for _mitigation in self.hold.personnel_slots
            if _mitigation.health > 0
        ]

        #  Update systems.

        self.oxygen.update(_mitigations)
        self.cells.update(_mitigations)
        self.heat_sink.update(_mitigations)
        self.hold.update(_mitigations)
        self.engine.update(_mitigations)
        self.cooler.update(_mitigations)
        self.life_support.update(_mitigations)

        for _module in self.optional_modules:
            _module.update(_mitigations)

    def module_report(self) -> dict[str, tuple[str, int, int]]:
        return module_logger.messages

    def personnel_report(self) -> dict[str, tuple[str, int, int]]:
        return module_logger.messages

    def short_report(self) -> dict[str, int]:
        """short_report

        Generates a short report for the crawler.

        Returns:
            dict[str, int]: The report.
        """
        _report: dict[str, int] = {}
        _report["cells"] = self.cells.level
        _report["oxygen"] = self.oxygen.level
        _report["terrain"] = self.engine.terrain
        _report["heat"] = self.heat_sink.level

        _report["cells_health"] = self.cells.health
        _report["engine_health"] = self.engine.health
        _report["cooler_health"] = self.cooler.health
        _report["life_support_health"] = self.life_support.health
        _report["hold_health"] = self.hold.health

        return _report

    def long_report(self) -> ModuleInfo:
        """long_report

        Generates a long report for the crawler.

        Returns:
            ModuleInfo: The report.
        """
        _report: ModuleInfo = ModuleInfo()

        #  Warning lights.

        _report.warning_light_levels = [
            self.cells.level,
            self.oxygen.level,
            self.engine.terrain,
            self.heat_sink.level,
            0,
            0,
        ]

        #  System dials.

        _report.dial_light_levels = [
            self.cells.level,
            self.oxygen.level,
            self.engine.revs_level,
            self.engine.speed_level,
            self.heat_sink.level,
        ]
        _report.dial_light_percent = [
            self.cells.power,
            self.oxygen.oxygen,
            self.engine.revs,
            self.engine.speed,
            self.heat_sink.heat,
        ]

        #  System lights.

        _report.system_light_levels = [
            self.cells.health_level,
            self.engine.health_level,
            self.cooler.health_level,
            self.life_support.health_level,
            self.hold.health_level,
        ]
        _report.system_light_percent = [
            self.cells.health,
            self.engine.health,
            self.cooler.health,
            self.life_support.health,
            self.hold.health,
        ]
        _report.system_light_status = [
            self.cells.status,
            self.engine.status,
            self.cooler.status,
            self.life_support.status,
            self.hold.status,
        ]

        #  Personnel.

        for _person in self.hold.personnel_slots:
            _report.personnel_light_texts.append((_person.name, f"{_person.role}"))
        for _person in self.hold.personnel_slots:
            _report.personnel_light_levels.append(_person.health_level)
        for _person in self.hold.personnel_slots:
            _report.personnel_light_percent.append(_person.health)
        for _person in self.hold.personnel_slots:
            _report.personnel_light_status.append(_person.status)

        #  Salvage.

        for _salvage in self.hold.salvage_slots:
            _report.salvage_light_texts.append((_salvage.name, _salvage.description))
        for _salvage in self.hold.salvage_slots:
            _report.salvage_light_levels.append(_salvage.health_level)
        for _salvage in self.hold.salvage_slots:
            _report.salvage_light_percent.append(_salvage.health)
        for _salvage in self.hold.salvage_slots:
            _report.salvage_light_status.append(_salvage.status)

        #  Optional modules.

        for _index, _module in enumerate(self.optional_modules):
            _report.optional_module_light_texts.append(
                (_module.name, _module.description, str(_module.class_level))
            )
            _report.optional_module_light_percent.append(_module.health)
            _report.optional_module_light_levels.append(_module.health_level)
            _report.optional_module_light_status.append(_module.status)

            _report.optional_module_light_actions.append(_module.toggle_online)

        return _report
