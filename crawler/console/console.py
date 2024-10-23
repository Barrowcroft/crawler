#  The Console class.

from random import randint
from typing import Callable

import pygame

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.command_line import CommandLine
from crawler.console.console_gui_components.base import Base
from crawler.console.console_gui_components.crawler_panel import CrawlerPanel
from crawler.console.console_gui_components.module_status_panel import \
    ModuleStatusPanel
from crawler.console.console_gui_components.options_panel import OptionsPanel
from crawler.console.console_gui_components.panel_with_two_buttons import \
    PanelWithTwoButtons
from crawler.console.console_gui_components.personnel_status_panel import \
    PersonnelStatusPanel
from crawler.console.inventory import Inventory
from crawler.console.map import Map
from crawler.console.menu import Menu
from crawler.console.status import Status
from crawler.console.terminal import Terminal
from crawler.crawler.system import ModuleInfo
from crawler.map.map_manager import MapManager
from crawler.terminal.terminal_manager import TerminalManager


class Console:
    """Console

    The Console class.

    The console is the main part of the game interface.
    It consists of a number of components.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(self, quit: Callable[[], None]) -> None:
        """__init__

        Initialises the Console.

        """

        #  Save quit method.

        self.quit: Callable[[], None] = quit

        #  Initialise the blink_flag variables.

        self.cycle_timer: float = 0
        self.cycle_blink: bool = False

        #  Layout the console.

        self.current_crawler_number: int = 1
        self.background: Base = Base()
        self.map: Map = Map()
        self.terminal: Terminal = Terminal()
        self.command_line: CommandLine = CommandLine()
        self.menu: Menu = Menu()
        self.inventory: Inventory = Inventory()
        self.status: Status = Status()

        #  Initialise the menu list.

        self.menu_list: list[tuple[str, Callable[[], None], bool]] = [  # type: ignore
            ("Options (ctrl-o)", self.toggle_options, False),
            ("Crawlers (ctrl-c)", self.toggle_crawlers, False),
            ("Personnel (ctrl-p)", self.toggle_personnel_report, False),
            ("Modules (Ctrl-m)", self.toggle_module_report, False),
            ("Start Scan (Ctrl-s)", self.start_scan, False),
            ("nop", None, True),
            ("nop", None, True),
            ("nop", None, True),
            ("nop", None, True),
            ("nop", None, True),
        ]

        #  Initialise the signal and scan flags.

        self.signal: bool = False
        self.scanning: bool = False
        self.last_scan_mode: str = "p"

        #  Initialise the confirmation Panel and side panels.

        self.confirmation: PanelWithTwoButtons = PanelWithTwoButtons()
        self.options_panel: OptionsPanel = OptionsPanel()
        self.crawlers_panel: CrawlerPanel = CrawlerPanel()
        self.module_status_panel: ModuleStatusPanel = ModuleStatusPanel()
        self.personnel_status_panel: PersonnelStatusPanel = PersonnelStatusPanel()

        # PROVLD settings

        self.satellite_id: str = (
            f"{str(randint(0,999)):0<3}-{str(randint(0,999)):0<3}-{str(randint(0,999)):0<3}"
        )

    def handleKeyEvent(self, event: pygame.event.Event) -> bool:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        ...

        if event.type == pygame.KEYDOWN:
            _keys = pygame.key.get_pressed()

            #  Menu options.

            if _keys[pygame.K_ESCAPE]:
                self.play_key_sound()
                if self.confirmation.showing is False:
                    self.confirm_quit()
                else:
                    self.confirmation.showing = False
                    return True
            elif self.confirmation.showing is True:
                self.confirmation.handleKeyEvent(event)
                return True

            elif (
                (_keys[pygame.K_LCTRL] or _keys[pygame.K_RCTRL])
                and _keys[pygame.K_o]
                and self.confirmation.showing is False
                and self.crawlers_panel.showing is False
                and self.module_status_panel.showing is False
                and self.personnel_status_panel.showing is False
            ):
                self.play_key_sound()
                self.toggle_options()
                return True
            elif self.options_panel.showing is True:
                self.options_panel.handleKeyEvent(event)
                return True

            elif (
                (_keys[pygame.K_LCTRL] or _keys[pygame.K_RCTRL])
                and _keys[pygame.K_c]
                and self.confirmation.showing is False
                and self.options_panel.showing is False
                and self.module_status_panel.showing is False
                and self.personnel_status_panel.showing is False
            ):
                self.play_key_sound()
                self.toggle_crawlers()
                return True
            elif self.crawlers_panel.showing is True:
                self.crawlers_panel.handleKeyEvent(event)
                self.current_crawler_number = self.crawlers_panel.current_crawler_number

            elif (
                (_keys[pygame.K_LCTRL] or _keys[pygame.K_RCTRL])
                and _keys[pygame.K_m]
                and self.confirmation.showing is False
                and self.options_panel.showing is False
                and self.crawlers_panel.showing is False
                and self.personnel_status_panel.showing is False
            ):
                self.play_key_sound()
                self.toggle_module_report()
                return True
            elif self.module_status_panel.showing is True:
                self.module_status_panel.handleKeyEvent(event)
                return True

            elif (
                (_keys[pygame.K_LCTRL] or _keys[pygame.K_RCTRL])
                and _keys[pygame.K_p]
                and self.confirmation.showing is False
                and self.crawlers_panel.showing is False
                and self.module_status_panel.showing is False
            ):
                self.play_key_sound()
                self.toggle_personnel_report()
                return True
            elif self.personnel_status_panel.showing is True:
                self.personnel_status_panel.handleKeyEvent(event)
                return True

            elif (_keys[pygame.K_LCTRL] or _keys[pygame.K_RCTRL]) and _keys[pygame.K_s]:
                self.play_key_sound()
                if self.scanning is False:
                    self.start_scan()
                    return True

            #  Layout options.

            elif _keys[pygame.K_LCTRL] and _keys[pygame.K_l]:
                self.play_key_sound()
                layout_config.save_current_layout()
                return True

            #  Sub panel options.

            elif (
                self.confirmation.showing is False
                and self.options_panel.showing is False
                and self.crawlers_panel.showing is False
                and self.personnel_status_panel.showing is False
                and self.module_status_panel.showing is False
            ):
                self.play_key_sound()
                self.inventory.handleKeyEvent(event)
                self.terminal.handleKeyEvent(event)
                self.command_line.handleKeyEvent(event)

            return False

    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.

        Args:
            event (pygame.event.Event): event to handle.
        """
        if self.confirmation.showing is True:
            self.confirmation.handleMouseEvent(event)
        elif self.options_panel.showing is True:
            self.options_panel.handleMouseEvent(event)
        elif self.crawlers_panel.showing is True:
            self.crawlers_panel.handleMouseEvent(event)
            self.current_crawler_number = self.crawlers_panel.current_crawler_number
        elif self.module_status_panel.showing is True:
            self.module_status_panel.handleMouseEvent(event)
        elif self.personnel_status_panel.showing is True:
            self.personnel_status_panel.handleMouseEvent(event)
        elif self.crawlers_panel.showing is True:
            self.crawlers_panel.handleMouseEvent(event)
        else:
            self.terminal.handleMouseEvent(event)

        self.menu.handleMouseEvent(event)
        self.inventory.handleMouseEvent(event)

    def update(
        self,
        dt: float,
        signal: bool,
        map_manager: MapManager,
        terminal_manager: TerminalManager,
        crawler_id: str,
        crawler_position: tuple[int, int],
        short_reports: list[dict[str, int]],
        long_report: ModuleInfo,
        module_report: dict[str, tuple[str, int, int]],
        personnel_report: dict[str, tuple[str, int, int]],
        pod_locations: list[tuple[int, int]],
        salvage_locations: list[tuple[int, int]],
    ) -> None:
        """update

        Update the Console

        Args:
            dt (float): delta time.
            signal (bool): indicates if there is a signal from the crawler. ie map is loaded.
            map_manager (MapManager): the map manager to display the map and sprites.
            terminal_manager (TerminalManager): the terminal manager to display the terminal.
            crawler_id (str): the id of the crawler.
            crawler_position (tuple[int, int]): the posiiton of the crawler.
            short_reports (list[dict[str, int]]): the short module infoe data from the crawlers.
            long_report (ModuleInfo): the long module infoe data from the System.
            module_report (dict[str, tuple[str, int, int]]): the status of the optional modules.
            personnel_report (dict[str, tuple[str, int, int]]): the status of the personnel.
            pod_locations (list[tuple[int, int]]): Location of pods for scanner.
            salvage_locations (list[tuple[int, int]]): Location of salvage for scanner.
        """

        #  Save singal value and scan data.

        self.signal = signal
        self.pod_locations: list[tuple[int, int]] = pod_locations
        self.salvage_locations: list[tuple[int, int]] = salvage_locations
        self.terminal_manager: TerminalManager = terminal_manager

        #  Update the delta time, and alternate blink_flag evey second.

        self.cycle_timer += dt
        if self.cycle_timer > 1:
            self.cycle_timer = 0
            self.cycle_blink = not self.cycle_blink
            if layout_config.alarm_sound_flag == True:
                if (
                    (self.status.warning_lights.request_alarm is True)
                    or (self.status.system_lights.request_beep is True)
                    or (self.inventory.module_lights.request_beep is True)
                    or (self.inventory.hold_lights.request_beep is True)
                    or (self.inventory.module_lights.request_beep is True)
                ):
                    layout_config.alarm_sound.play()

        self.background.update_base(
            c.CONSOLE_SCREEN_SIZE,
            colour=layout_config.colour,
            frame_flag=layout_config.frame_flag,
            background_flag=layout_config.background_flag,
        )

        #  Console panels.

        self.map.update_map(
            dt,
            map_manager,
            layout_config.map_position,
            signal_flag=self.signal,
            scanlines_flag=layout_config.scanlines_flag,
            satellite_id=self.satellite_id,
            crawler_position=crawler_position,
        )

        self.terminal.update_terminal(
            layout_config.terminal_position,
            terminal_manager=terminal_manager,
            signal_flag=self.signal,
            crawler_id=crawler_id,
        )

        self.command_line.update_command_line(
            dt,
            layout_config.terminal_position,
        )

        self.menu.update_menu(
            layout_config.menu_position,
            signal_flag=self.signal,
            menu=self.menu_list,
        )

        self.inventory.update_inventory(
            layout_config.inventory_position,
            personnel_light_texts=long_report.personnel_light_texts,
            personnel_light_levels=long_report.personnel_light_levels,
            personnel_light_percent=long_report.personnel_light_percent,
            personnel_light_status=long_report.personnel_light_status,
            salvage_light_texts=long_report.salvage_light_texts,
            salvage_light_levels=long_report.salvage_light_levels,
            salvage_light_percent=long_report.salvage_light_percent,
            salvage_light_status=long_report.salvage_light_status,
            module_light_texts=long_report.optional_module_light_texts,
            module_light_levels=long_report.optional_module_light_levels,
            module_light_percent=long_report.optional_module_light_percent,
            module_light_status=long_report.optional_module_light_status,
            module_light_actions=long_report.optional_module_light_actions,
            signal_flag=self.signal,
            blink_flag=self.cycle_blink,
            crawler_id=crawler_id,
        )

        self.status.update_status(
            dt,
            map_manager,
            layout_config.status_position,
            crawler_position=crawler_position,
            warning_light_levels=long_report.warning_light_levels,
            system_light_levels=long_report.system_light_levels,
            system_light_percent=long_report.system_light_percent,
            system_light_status=long_report.system_light_status,
            dial_light_levels=long_report.dial_light_levels,
            dial_light_percent=long_report.dial_light_percent,
            blink_flag=self.cycle_blink,
            signal_flag=self.signal,
        )

        #  Sliding panels.

        self.confirmation.update_panel(
            dt,
            (
                layout_config.map_position[0],
                layout_config.map_position[1],
                500,
                150,
            ),
            (self.accept_quit, self.cancel_quit),
            "bottom",
            "Are you sure you want to quit Crawler?",
            ("Yes", "No"),
            ("y", "n"),
        )

        self.options_panel.update_panel(
            dt,
            (
                int((1920 - 766) / 2),
                60,
                766,
                598,
            ),
            "top",
        )

        self.module_status_panel.update_panel(
            dt,
            (
                layout_config.map_position[0],
                layout_config.map_position[1],
                900,
                466,
            ),
            module_report,
            "bottom",
            self.cycle_blink,
        )

        self.personnel_status_panel.update_panel(
            dt,
            (
                layout_config.map_position[0],
                layout_config.map_position[1],
                900,
                394,
            ),
            personnel_report,
            "bottom",
            self.cycle_blink,
        )

        self.crawlers_panel.update_panel(
            dt,
            (
                layout_config.map_position[0],
                layout_config.map_position[1],
                250,
                550,
            ),
            short_reports,
            "left",
            self.cycle_blink,
        )

        #  Restet menu.

        if self.options_panel.showing is True:
            self.menu.disable_all()
            self.menu.enable(c.CONSOLE_OPTIONS_MENU_INDEX)
        if self.crawlers_panel.showing is True:
            self.menu.disable_all()
            self.menu.enable(c.CONSOLE_CRAWLERS_MENU_INDEX)
        if self.personnel_status_panel.showing is True:
            self.menu.disable_all()
            self.menu.enable(c.CONSOLE_PERSONNEL_MENU_INDEX)
        if self.module_status_panel.showing is True:
            self.menu.disable_all()
            self.menu.enable(c.CONSOLE_MODULES_MENU_INDEX)
        if self.scanning is True:
            self.menu.disable_all()

    def render(self, display: pygame.Surface, actualFPS: float) -> None:
        """render

        Renders the Console.

        Args:
            display (pygame.event.Event): display on which to render.
            actualFPS (float): actual frames per second.
        """

        #  Create the panels.

        self.background.render(display)
        self.map.render(display, actualFPS)
        self.terminal.render(display)
        self.command_line.render(display)
        self.menu.render(display)
        self.inventory.render(display)
        self.status.render(display)
        self.options_panel.render(display)
        self.module_status_panel.render(display)
        self.personnel_status_panel.render(display)
        self.crawlers_panel.render(display)
        self.confirmation.render(display)

    #  Functions that may be called from functions in the parent class.

    # #  TERMINAL

    # def set_terminal_buffer_index(self, index: int) -> None:
    #     """set_terminal_buffer_index

    #     Sets which message is at the top of the terminal.

    #     Args:
    #         index (int): index to set
    #     """
    #     self.terminal.set_terminal_buffer_index(index)

    # def set_terminal_prompt(self, prompt: str) -> None:
    #     """set_terminal_prompt

    #     Set the  terminal prompt.

    #     Args:
    #         index (int): prompt to set
    #     """
    #     self.command_line.set_terminal_prompt(prompt)

    #  SCAN

    def do_scan(self, mode: str) -> None:
        """do_scan

        Starts the minimap scan, passing the coordinate of the targets to find.

        Args:
            scan_targets (list[tuple[int, int]]): scan targets
        """
        if self.scanning is True:
            self.terminal_manager.message(2, "Scanning already in progress...")
            return

        self.last_scan_mode = mode
        _locations: list[tuple[int, int]] = []

        if mode == "p":
            _locations: list[tuple[int, int]] = self.pod_locations
            self.terminal_manager.message(2, "Scanning for escape pods...")
        if mode == "s":
            _locations: list[tuple[int, int]] = self.salvage_locations
            self.terminal_manager.message(2, "Scanning for salvage...")
        self.menu.disable_all()
        self.status.minimap.start_scan(scan_targets=_locations, callback=self.end_scan)

        if layout_config.scanner_sound_flag is True:
            layout_config.scan_sound.set_volume(0.5)
            layout_config.scan_sound.play()

        self.scanning: bool = True

    def abort_scan(self) -> None:
        self.scanning = False
        self.status.minimap.abort_scan()
        layout_config.scan_sound.stop()
        self.menu.enable_all()

    def end_scan(self) -> None:
        """end_scan

        Call back for the scan routine when finished scanning.

        Args:
            scan_targets (list[tuple[int, int]]): scan targets
        """
        layout_config.scan_sound.fadeout(250)

        self.scanning = False

        self.menu.enable_all()

    def start_scan(self) -> None:

        self.do_scan(self.last_scan_mode)

    #  QUIT

    def confirm_quit(self) -> None:
        self.confirmation.showing = True
        self.options_panel.showing = False
        self.crawlers_panel.showing = False
        self.personnel_status_panel.showing = False
        self.module_status_panel.showing = False
        self.abort_scan()

    def accept_quit(self) -> None:
        layout_config.scan_sound.stop()
        self.quit()

    def cancel_quit(self) -> None:
        self.confirmation.showing = False
        self.menu.enable_all()

    #  MENU

    def toggle_options(self) -> None:
        self.options_panel.showing = not self.options_panel.showing

        if self.options_panel.showing is True:
            self.menu.disable_all_but(c.CONSOLE_OPTIONS_MENU_INDEX)
            self.confirmation.showing = False
            self.crawlers_panel.showing = False
            self.personnel_status_panel.showing = False
            self.module_status_panel.showing = False
            self.abort_scan()
        else:
            self.menu.enable_all()

    def toggle_crawlers(self) -> None:
        self.crawlers_panel.showing = not self.crawlers_panel.showing

        if self.crawlers_panel.showing is True:
            self.menu.disable_all_but(c.CONSOLE_CRAWLERS_MENU_INDEX)
            self.confirmation.showing = False
            self.options_panel.showing = False
            self.personnel_status_panel.showing = False
            self.module_status_panel.showing = False
        else:
            self.menu.enable_all()

    def toggle_personnel_report(self) -> None:
        self.personnel_status_panel.showing = not self.personnel_status_panel.showing
        if self.personnel_status_panel.showing is True:
            self.menu.disable_all_but(c.CONSOLE_PERSONNEL_MENU_INDEX)
            self.confirmation.showing = False
            self.options_panel.showing = False
            self.crawlers_panel.showing = False
            self.module_status_panel.showing = False
        else:
            self.menu.enable_all()

    def toggle_module_report(self) -> None:
        self.module_status_panel.showing = not self.module_status_panel.showing
        if self.module_status_panel.showing is True:
            self.menu.disable_all_but(c.CONSOLE_MODULES_MENU_INDEX)
            self.confirmation.showing = False
            self.options_panel.showing = False
            self.crawlers_panel.showing = False
            self.personnel_status_panel.showing = False
        else:
            self.menu.enable_all()

    def play_key_sound(self) -> None:
        if layout_config.key_sound_flag is True:
            layout_config.key_sound.play()
