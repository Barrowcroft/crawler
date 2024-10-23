#  Process command executes commands from the console terminal.

from typing import Callable

from crawler.crawler.crawler import Crawler


def show_hold(
    buffer: list[tuple[int, str]],
    num: str,
    crawlers: list[Crawler],
) -> list[tuple[int, str]]:

    crawler_num: int = 0

    if num.isdigit():
        crawler_num = int(num.strip())
    else:
        return buffer + [(3, f"*** Invalid crawler number: {num}")]

    if crawler_num > len(crawlers) or crawler_num < 1:
        return buffer + [(3, f"*** Unrecognised crawler number: {crawler_num}")]
    else:
        report = crawlers[crawler_num - 1].system.long_report()
        buffer += [(2, f"Hold report for {crawlers[crawler_num-1].identifier}")]
        for _index, _location in enumerate(report.salvage_light_texts):
            buffer += [
                (
                    2,
                    f"   Location {_index}   {_location[0] + ', ' + _location[1]:50} Helth {report.salvage_light_percent[_index]:4}% - {report.salvage_light_status[_index]}",
                )
            ]
    return buffer


def show_modules(
    buffer: list[tuple[int, str]],
    num: str,
    crawlers: list[Crawler],
) -> list[tuple[int, str]]:

    crawler_num: int = 0

    if num.isdigit():
        crawler_num = int(num.strip())
    else:
        return buffer + [(3, f"*** Invalid crawler number: {num}")]

    if crawler_num > len(crawlers) or crawler_num < 1:
        return buffer + [(3, f"*** Unrecognised crawler number: {crawler_num}")]
    else:
        report = crawlers[crawler_num - 1].system.long_report()
        buffer += [
            (2, f"Optional modules report for {crawlers[crawler_num-1].identifier}")
        ]
        for _index, _module in enumerate(report.optional_module_light_texts):
            buffer += [
                (
                    2,
                    f"   Location {_index}   {_module[0] + ', ' + _module[1] + '[Level ' + _module[2] +']':50} Helth {report.optional_module_light_percent[_index]:4}% - {report.optional_module_light_status[_index]}",
                )
            ]
    return buffer


def show_personnel(
    buffer: list[tuple[int, str]],
    num: str,
    crawlers: list[Crawler],
) -> list[tuple[int, str]]:

    crawler_num: int = 0

    if num.isdigit():
        crawler_num = int(num.strip())
    else:
        return buffer + [(3, f"*** Invalid crawler number: {num}")]

    if crawler_num > len(crawlers) or crawler_num < 1:
        return buffer + [(3, f"*** Unrecognised crawler number: {crawler_num}")]
    else:
        report = crawlers[crawler_num - 1].system.long_report()
        buffer += [(2, f"Personnel report for {crawlers[crawler_num-1].identifier}")]
        for _index, _personnel in enumerate(report.personnel_light_texts):
            buffer += [
                (
                    2,
                    f"   Location {_index}   {_personnel[0] + ', ' + _personnel[1]:40}  Health {report.personnel_light_percent[_index]:4}% - {report.personnel_light_status[_index]}",
                )
            ]
    return buffer


def show_dials(
    buffer: list[tuple[int, str]],
    num: str,
    crawlers: list[Crawler],
) -> list[tuple[int, str]]:

    crawler_num: int = 0

    if num.isdigit():
        crawler_num = int(num.strip())
    else:
        return buffer + [(3, f"*** Invalid crawler number: {num}")]

    if crawler_num > len(crawlers) or crawler_num < 1:
        return buffer + [(3, f"*** Unrecognised crawler number: {crawler_num}")]
    else:
        report = crawlers[crawler_num - 1].system.long_report()

        buffer += [(2, f"Dials report for {crawlers[crawler_num-1].identifier}")]
        buffer += [
            (
                2,
                f"   cells:   reading {report.dial_light_percent[0]:4}%",
            )
        ]
        buffer += [
            (
                2,
                f"   oxygen:  reading {report.dial_light_percent[1]:4}% ",
            )
        ]
        buffer += [
            (
                2,
                f"   revs:    reading {report.dial_light_percent[2]:4}%",
            )
        ]
        buffer += [
            (
                2,
                f"   speed:   reading {report.dial_light_percent[3]:4}%",
            )
        ]
        buffer += [
            (
                2,
                f"   heat:    reading {report.dial_light_percent[4]:4}%",
            )
        ]
    return buffer


def show_system(
    buffer: list[tuple[int, str]],
    num: str,
    crawlers: list[Crawler],
) -> list[tuple[int, str]]:

    crawler_num: int = 0

    if num.isdigit():
        crawler_num = int(num.strip())
    else:
        return buffer + [(3, f"*** Invalid crawler number: {num}")]

    if crawler_num > len(crawlers) or crawler_num < 1:
        return buffer + [(3, f"*** Unrecognised crawler number: {crawler_num}")]
    else:
        report = crawlers[crawler_num - 1].system.long_report()
        buffer += [
            (2, f"System module report for {crawlers[crawler_num-1].identifier}")
        ]
        buffer += [
            (
                2,
                f"   cells:         health {report.system_light_percent[0]:4}% - {report.system_light_status[0]}",
            )
        ]
        buffer += [
            (
                2,
                f"   engine:        health {report.system_light_percent[1]:4}% - {report.system_light_status[1]}",
            )
        ]
        buffer += [
            (
                2,
                f"   cooler:        health {report.system_light_percent[2]:4}% - {report.system_light_status[2]}",
            )
        ]
        buffer += [
            (
                2,
                f"   life support:  health {report.system_light_percent[3]:4}% - {report.system_light_status[3]}",
            )
        ]
        buffer += [
            (
                2,
                f"   hold:          health {report.system_light_percent[4]:4}% - {report.system_light_status[4]}",
            )
        ]
    return buffer


def show_warnings(
    buffer: list[tuple[int, str]],
    num: str,
    crawlers: list[Crawler],
) -> list[tuple[int, str]]:

    crawler_num: int = 0

    if num.isdigit():
        crawler_num = int(num.strip())
    else:
        return buffer + [(3, f"*** Invalid crawler number: {num}")]

    if crawler_num > len(crawlers) or crawler_num < 1:
        return buffer + [(3, f"*** Unrecognised crawler number: {crawler_num}")]
    else:
        report = crawlers[crawler_num - 1].system.short_report()
        buffer += [
            (2, f"Warning light report for {crawlers[crawler_num-1].identifier}")
        ]
        buffer += [(2, f"   cells:    level {report['cells']}")]
        buffer += [(2, f"   oxygen:   level {report['oxygen']}")]
        buffer += [(2, f"   terrain:  level {report['terrain']}")]
        buffer += [(2, f"   heat:     level {report['heat']}")]
        buffer += [(2, f"[0=Normal, 1=Alert,  2=Warning,  3=Danger]")]
    return buffer


def show(
    buffer: list[tuple[int, str]],
    command: str,
    crawlers: list[Crawler],
) -> list[tuple[int, str]]:
    command = command.strip()

    if command.lower().startswith("dials"):
        buffer = show_dials(buffer, command[6:], crawlers)
    elif command.lower().startswith("hold"):
        buffer = show_hold(buffer, command[5:], crawlers)
    elif command.lower().startswith("modules"):
        buffer = show_modules(buffer, command[8:], crawlers)
    elif command.lower().startswith("personnel"):
        buffer = show_personnel(buffer, command[10:], crawlers)
    elif command.lower().startswith("system"):
        buffer = show_system(buffer, command[7:], crawlers)
    elif command.lower().startswith("warnings"):
        buffer = show_warnings(buffer, command[9:], crawlers)
    else:
        buffer += [(3, f"*** Unrecognised option: {command}")]
    return buffer


def scan(
    buffer: list[tuple[int, str]],
    command: str,
    start_scan: Callable[[str], None],
) -> list[tuple[int, str]]:
    command = command.strip()

    if command.lower().startswith("-p"):
        start_scan("p")
    elif command.lower().startswith("-s"):
        start_scan("s")
    else:
        buffer += [(3, f"*** Unrecognised scan target: {command}")]

    return buffer


def describe_module(
    module: str, buffer: list[tuple[int, str]], num: str, crawlers: list[Crawler]
) -> list[tuple[int, str]]:

    crawler_num: int = 0

    if num.isdigit():
        crawler_num = int(num.strip())
    else:
        return buffer + [(3, f"*** Invalid crawler number: {num}")]

    if crawler_num > len(crawlers) or crawler_num < 1:
        return buffer + [(3, f"*** Unrecognised crawler number: {crawler_num}")]
    else:
        _module = crawlers[crawler_num].system.cells
        if module == "cells":
            _module = crawlers[crawler_num].system.cells
        if module == "engine":
            _module = crawlers[crawler_num].system.engine
        if module == "cooler":
            _module = crawlers[crawler_num].system.cooler
        if module == "life-support":
            _module = crawlers[crawler_num].system.life_support
        if module == "hold":
            _module = crawlers[crawler_num].system.hold
        if module == "module1":
            _module = crawlers[crawler_num].system.optional_modules[0]
        if module == "module2":
            _module = crawlers[crawler_num].system.optional_modules[1]
        if module == "module3":
            _module = crawlers[crawler_num].system.optional_modules[2]
        if module == "module4":
            _module = crawlers[crawler_num].system.optional_modules[3]
        if module == "module5":
            _module = crawlers[crawler_num].system.optional_modules[4]
        if module == "module6":
            _module = crawlers[crawler_num].system.optional_modules[5]

        buffer += [
            (
                2,
                f"Module description for {_module.name} [Level {_module.class_level}] for {crawlers[crawler_num-1].identifier}",
            )
        ]
        buffer += [(2, f"{_module.information}")]

        buffer += [(2, f"   Status = {_module.status}")]

        buffer += [
            (
                2,
                f"   Health (Actual/Max) = {_module.health}/{_module.max_health}",
            )
        ]
        buffer += [
            (
                2,
                f"   Oxygen:  withdrawal = {_module.oxygen_withdrawal:2}  deposit = {_module.oxygen_deposit:2}",
            )
        ]
        buffer += [
            (
                2,
                f"   Power:   withdrawal = {_module.power_withdrawal:2}  deposit = {_module.power_deposit:2}",
            )
        ]
        buffer += [
            (
                2,
                f"   Heat:    withdrawal = {_module.heat_withdrawal:2}  deposit = {_module.heat_deposit:2}",
            )
        ]
        if _module.power_withdrawal_essential is True:
            buffer += [
                (
                    2,
                    f"If this module cannot withdraw power it will go off line.",
                )
            ]
        if _module.power_deposit_essential is True:
            buffer += [
                (
                    2,
                    f"If this module cannot deposit power it will go off line.",
                )
            ]
        if _module.oxygen_withdrawal_essential is True:
            buffer += [
                (
                    2,
                    f"If this module cannot withdraw oxygen it will go off line.",
                )
            ]
        if _module.oxygen_deposit_essential is True:
            buffer += [
                (
                    2,
                    f"If this module cannot deposit oxygen it will go off line.",
                )
            ]
        if _module.heat_withdrawal_essential is True:
            buffer += [
                (
                    2,
                    f"If this module cannot withdraw heat it will go off line.",
                )
            ]
        if _module.heat_deposit_essential is True:
            buffer += [
                (
                    2,
                    f"If this module cannot deposit heat it will go off line.",
                )
            ]
        buffer += [
            (
                2,
                f"If this module is taking damage the {_module.mitigation} will stop it failing completely.",
            )
        ]

    return buffer


def describe(
    buffer: list[tuple[int, str]],
    command: str,
    crawlers: list[Crawler],
) -> list[tuple[int, str]]:
    command = command.strip()

    command = command.strip()

    if command.lower().startswith("cells"):
        buffer = describe_module("cells", buffer, command[6:], crawlers)
    elif command.lower().startswith("engine"):
        buffer = describe_module("engine", buffer, command[7:], crawlers)
    elif command.lower().startswith("cooler"):
        buffer = describe_module("cooler", buffer, command[7:], crawlers)
    elif command.lower().startswith("life-support"):
        buffer = describe_module("life-support", buffer, command[13:], crawlers)
    elif command.lower().startswith("hold"):
        buffer = describe_module("hold", buffer, command[5:], crawlers)
    elif command.lower().startswith("module1"):
        buffer = describe_module("module1", buffer, command[8:], crawlers)
    elif command.lower().startswith("module2"):
        buffer = describe_module("module2", buffer, command[8:], crawlers)
    elif command.lower().startswith("module3"):
        buffer = describe_module("module3", buffer, command[8:], crawlers)
    elif command.lower().startswith("module4"):
        buffer = describe_module("module4", buffer, command[8:], crawlers)
    elif command.lower().startswith("module5"):
        buffer = describe_module("module8", buffer, command[8:], crawlers)
    elif command.lower().startswith("module6"):
        buffer = describe_module("module6", buffer, command[8:], crawlers)
    else:
        buffer += [(3, f"*** Unrecognised option: {command}")]

    return buffer


def process_command(
    buffer: list[tuple[int, str]],
    command: str,
    crawlers: list[Crawler],
    current_crawler: int,
    confirm_exit: Callable[[], None],
    toggle_options: Callable[[], None],
    toggle_crawlers: Callable[[], None],
    toggle_personnel: Callable[[], None],
    toggle_modules: Callable[[], None],
    start_scan: Callable[[str], None],
) -> list[tuple[int, str]]:

    if command.lower() == "help":
        buffer.append((2, "Currently available commands:"))
        buffer.append((2, "   clear..................... clears the terminal"))
        buffer.append((2, "   crawlers.................. show crawler status panel"))
        buffer.append((2, "   current................... indentify current crawler"))
        buffer.append(
            (2, "   describe cells n.......... describe power cells in crawler n")
        )
        buffer.append((2, "   describe cooler n......... describe cooler in crawler n"))
        buffer.append((2, "   describe engine n......... describe engine in crawler n"))
        buffer.append((2, "   describe hold  n.......... describe hold in crawler n"))
        buffer.append(
            (2, "   describe life-support n... describe life-support in crawler n")
        )
        buffer.append(
            (2, "   describe module1 n........ describe module1 (etc.) in crawler n")
        )
        buffer.append((2, "   help...................... list available comands"))
        buffer.append((2, "   modules................... show module status panel"))
        buffer.append((2, "   options................... show options panel"))
        buffer.append((2, "   personnel................. show personnel status panel"))
        buffer.append((2, "   quit...................... quit crawler"))
        buffer.append((2, "   scan -p................... scan for escape pods"))
        buffer.append((2, "   scan -s................... scan for salvage"))
        buffer.append((2, "   show dials n.............. show dials for crawler 'n'"))
        buffer.append((2, "   show hold n............... show hold for crawler 'n'"))
        buffer.append(
            (2, "   show modules n............ show optional modules for crawler 'n'")
        )
        buffer.append(
            (2, "   show personnel n.......... show personnel for crawler 'n'")
        )
        buffer.append(
            (2, "   show system n............. show system modules for crawler 'n'")
        )
        buffer.append(
            (2, "   show warnings n........... show warnings for crawler 'n'")
        )
        buffer.append((2, f"Press 'CTRL-UP' or 'CTRL-DOWN' to scroll terminal history"))
        buffer.append(
            (2, f"Press 'ALT-UP' or 'ALT-DOWN' to scroll command line history")
        )
        return buffer

    elif command.lower() == "clear":
        return []

    elif command.lower() == "quit":
        confirm_exit()
        return buffer

    elif command.lower() == "crawlers":
        toggle_crawlers()
        buffer.append((2, f"Current crawler is:"))
        buffer.append((2, f"   {crawlers[current_crawler-1].identifier}"))
        return buffer

    elif command.lower() == "current":
        buffer.append((2, f"Current crawler is:"))
        buffer.append((2, f"   {crawlers[current_crawler-1].identifier}"))
        return buffer

    elif command.lower().startswith("describe"):
        buffer = describe(buffer, command[9:], crawlers)
        return buffer

    elif command.lower() == "modules":
        toggle_modules()
        return buffer

    elif command.lower() == "options":
        toggle_options()
        return buffer

    elif command.lower() == "personnel":
        toggle_personnel()
        return buffer

    elif command.lower().startswith("scan"):
        buffer = scan(buffer, command[5:], start_scan)
        return buffer

    elif command.lower().startswith("show"):
        buffer = show(buffer, command[5:], crawlers)
        return buffer

    else:
        buffer.append((3, f"*** Unrecognised command: {command}"))
        return buffer
