#  The Terminal Manager class handles the processing of commands in the temrinal and presentation of results.

from typing import Callable

import pygame

import crawler.constants as c
from crawler.crawler.crawler import Crawler
from crawler.terminal.process_command import process_command


class TerminalManager:
    """TerminalManager

    The Terminal Manager class handles the processing of commands in the temrinal and presentation of results.

    """

    def __init__(self) -> None:

        self.command: str = ""
        self.command_history: list[str] = []
        self.command_history_index: int = 0

        self.buffer: list[tuple[int, str]] = []
        self.buffer_index: int = 0

        self.crawlers: list[Crawler] = []
        self.current_crawler: int = 0

        self.message(1, f"Remote Crawler Monitor (c) PROVLD v.65.17")
        self.message(1, f"Type 'help' for a list of commands")

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.

        Args:
            event (pygame.event.Event): event to handle.
        """

        #  When a key is presssed if the key press represents a printable
        #  ie, is not Return or Backpace, then if it is alpanumeric or space
        #  add it to the buffer. If the key press is Return then trim the string and return it.
        #  If the key press is backspace then remove the last character from the buffer.
        #  If the key press is return then process the command.

        if event.type == pygame.KEYDOWN:
            _keys = pygame.key.get_pressed()

            if (
                event.key != pygame.K_RETURN
                and event.key != pygame.K_BACKSPACE
                and event.key != pygame.K_UP
                and event.key != pygame.K_DOWN
                and event.key != pygame.K_LEFT
                and event.key != pygame.K_RIGHT
            ):
                if event.unicode.isalnum():
                    self.command += pygame.key.name(event.key)
                if event.key == pygame.K_SPACE:
                    self.command += " "
                if event.key == pygame.K_MINUS:
                    self.command += "-"

            elif (_keys[pygame.K_RALT] or _keys[pygame.K_LALT]) and _keys[pygame.K_UP]:
                self.restore_from_command_history(-1)
            elif (_keys[pygame.K_RALT] or _keys[pygame.K_LALT]) and _keys[
                pygame.K_DOWN
            ]:
                self.restore_from_command_history(1)
            elif event.key == pygame.K_RETURN:
                self.command = self.command.strip()
                self.buffer += [(1, self.command)]
                self.buffer = process_command(
                    self.buffer,
                    self.command,
                    self.crawlers,
                    self.current_crawler,
                    self.confirm_exit,
                    self.toggle_options,
                    self.toggle_crawlers,
                    self.toggle_personnel,
                    self.toggle_modules,
                    self.start_scan,
                )
                self.buffer_index = len(self.buffer) - c.TERMINAL_LINES_TO_SHOW
                if self.buffer_index < 0:
                    self.buffer_index = 0
                self.add_to_command_history(self.command)
                self.command = ""

            elif event.key == pygame.K_BACKSPACE:
                self.command = self.command[: len(self.command) - 1]

    def update(
        self,
        crawlers: list[Crawler],
        current_crawler: int,
        confirm_exit: Callable[[], None],
        toggle_options: Callable[[], None],
        toggle_crawlers: Callable[[], None],
        toggle_perssonnel: Callable[[], None],
        toggle_modules: Callable[[], None],
        set_command_buffer: Callable[[str], None],
        start_scan: Callable[[str], None],
    ) -> None:
        self.crawlers = crawlers
        self.current_crawler = current_crawler
        self.confirm_exit: Callable[[], None] = confirm_exit
        self.toggle_options: Callable[[], None] = toggle_options
        self.toggle_crawlers: Callable[[], None] = toggle_crawlers
        self.toggle_personnel: Callable[[], None] = toggle_perssonnel
        self.toggle_modules: Callable[[], None] = toggle_modules
        self.set_command_buffer: Callable[[str], None] = set_command_buffer
        self.start_scan: Callable[[str], None] = start_scan

    def message(self, level: int, text: str) -> None:
        self.buffer += [(level, text)]
        self.buffer_index = len(self.buffer) - c.TERMINAL_LINES_TO_SHOW
        if self.buffer_index < 0:
            self.buffer_index = 0

    def update_command_buffer(self, command: str) -> None:
        self.command = command
        self.set_command_buffer(command)

    def add_to_command_history(self, command: str) -> None:
        if command not in self.command_history:
            self.command_history.append(command)
        self.command_history_index = len(self.command_history)

    def restore_from_command_history(self, step: int) -> None:
        if len(self.command_history) == 0:
            return

        self.command_history_index += step
        self.command_history_index = (
            0 if self.command_history_index < 0 else self.command_history_index
        )
        self.command_history_index = (
            len(self.command_history) - 1
            if self.command_history_index > len(self.command_history) - 1
            else self.command_history_index
        )
        self.update_command_buffer(self.command_history[self.command_history_index])
