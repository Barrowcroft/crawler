#  The Main game state.

import pygame  # type: ignore
import pygame.event  # type: ignore

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.console.console import Console
from crawler.crawler.crawler import Crawler
from crawler.map.map_manager import MapManager
from crawler.states.state import State
from crawler.terminal.terminal_manager import TerminalManager


class Main(State):
    """Main

    Args:
        State: this subclasses State.
    """

    #  PROPERTIES

    @property
    def nextState(self) -> str:
        """nextState

        Gets the next game state.

        Returns:
            str: the next game state.
        """
        return self._nextState

    #  GAME LOOP METHODS

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(self) -> None:
        """__init__

        Initialises the game state.

        """

        #  Initialise variables.

        self._nextState: str = ""
        self._done: bool = False

        #  Initialise the Crawlers.

        self.crawlers: list[Crawler] = []
        self.current_crawler_number: int = 1
        self.connecting: bool = False
        self.connecting_timer: float = 0

        for number in range(9):
            self.crawlers.append(Crawler(number))  #  type: ignore

        #  Send message to terminal.
        self.terminal_manager: TerminalManager = TerminalManager()
        self.terminal_manager.message(1, f"Connecting to crawler CRWLR01...")

        #  Initialise the Map.

        self.map_manager: MapManager = MapManager(
            c.LEVEL_ONE_MAP_FILENAME, self.crawlers
        )

        #  Initialise the Console.

        self.console: Console = Console(self.quit)

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.
        Coordinates the handling of events by other classes.

        Args:
            event (pygame.event.Event): event to handle.
        """

        _handled: bool = False
        _handled = self.console.handleKeyEvent(event)

        if (
            _handled is False
            and self.console.confirmation.showing is False
            and self.console.options_panel.showing is False
            and self.console.crawlers_panel.showing is False
            and self.console.personnel_status_panel.showing is False
            and self.console.module_status_panel.showing is False
        ):
            self.terminal_manager.handleKeyEvent(event)

        if self.current_crawler_number != self.console.current_crawler_number:
            self.crawlers[int(self.current_crawler_number) - 1].stop()
            self.current_crawler_number = self.console.current_crawler_number
            self.connecting = True
            self.connecting_timer = 0
            self.terminal_manager.message(
                1, f"Connecting to crawler CRWLR{self.current_crawler_number:02}..."
            )
        self.crawlers[int(self.current_crawler_number) - 1].handleKeyEvent(event)

    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.
        Coordinates the handling of events by other classes.

        Args:
            event (pygame.event.Event): event to handle.
        """
        self.console.handleMouseEvent(event)

    def update(self, dt: float) -> None:
        """udate

        Updates the class.
        Coordinates the updating of all other classes.

        Args:
            dt (float): delta time
        """

        for _crawler in self.crawlers:
            _crawler.update(dt)

        _signal: bool = False
        if self.map_manager.loaded is True:
            if self.connecting is False:
                _signal = True
            else:
                self.connecting_timer += dt
                if self.connecting_timer > 1:
                    self.connecting = False
                    self.connecting_timer = 0
                    _signal = True
                else:
                    _signal = False

        _crawler_num: int = int(self.current_crawler_number) - 1

        _short_reports: list[dict[str, int]] = []
        for _crawler in self.crawlers:
            _short_reports.append(_crawler.system.short_report())

        self.console.update(
            dt,
            _signal,
            self.map_manager,
            self.terminal_manager,
            self.crawlers[_crawler_num].identifier,
            (
                int(self.crawlers[_crawler_num].position.x),
                int(self.crawlers[_crawler_num].position.y),
            ),
            _short_reports,
            self.crawlers[_crawler_num].system.long_report(),
            self.crawlers[_crawler_num].system.module_report(),
            self.crawlers[_crawler_num].system.personnel_report(),
            self.map_manager.pod_locations,
            self.map_manager.salvage_locations,
        )
        self.crawlers[_crawler_num].system.short_report()
        self.terminal_manager.update(
            self.crawlers,
            self.current_crawler_number,
            self.console.confirm_quit,
            self.console.toggle_options,
            self.console.toggle_crawlers,
            self.console.toggle_personnel_report,
            self.console.toggle_module_report,
            self.console.command_line.set_command_buffer,
            self.console.do_scan,
        )

    def render(self, display: pygame.Surface, actualFPS: float) -> None:  # type: ignore
        """render

        Renders the class.
        Coordinates the rendering of all other classes.

        Args:
            display (pygame.event.Event): display on which to render.
            actualFPS (float): actual frames per second.
        """
        self.console.render(display, actualFPS)

    def quit(self) -> None:
        self._done = True

    def checkDone(self) -> bool:
        """checkDone

        Checks if the current state is completed.

        Returns:
            bool: true if completed.
        """

        if self._done:
            self._nextState = c.GAME_END
        return self._done
