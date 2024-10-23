#  The Terminal class.

import pygame

import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.display_terminal_buffer import (
    display_terminal_buffer,
)
from crawler.console.console_tools.show_text import show_text
from crawler.terminal.terminal_manager import TerminalManager

BLACK = (0, 0, 0)


class Terminal(Base):
    """Terminal

    The Terminal class.

    Args:
        Base: The Terminal class subclasses the Base class.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(
        self,
    ) -> None:
        """__init__

        Initialises the Terminal class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise crawler id.

        self.crawler_id: str = ""

    def handleKeyEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleKeyEvent

        Handles keyboard events.

        Args:
            event (pygame.event.Event): event to handle.
        """

        #  Process line up and line down key presses.

        if event.type == pygame.KEYDOWN:
            _keys = pygame.key.get_pressed()
            if (_keys[pygame.K_LCTRL] or _keys[pygame.K_RCTRL]) and _keys[pygame.K_UP]:
                self.terminal_manager.buffer_index -= 1
                if self.terminal_manager.buffer_index < 0:
                    self.terminal_manager.buffer_index = 0
            elif (_keys[pygame.K_LCTRL] or _keys[pygame.K_RCTRL]) and _keys[
                pygame.K_DOWN
            ]:
                self.terminal_manager.buffer_index += 1
                if self.terminal_manager.buffer_index >= len(
                    self.terminal_manager.buffer
                ):
                    self.terminal_manager.buffer_index = (
                        len(self.terminal_manager.buffer) - 1
                    )

    def handleMouseEvent(self, event: pygame.event.Event) -> None:  # type: ignore
        """handleMouseEvent

        Handles mouse events.

        Args:
            event (pygame.event.Event): event to handle.
        """

        #  Process line up and line down for mousewheel.

        if event.type == pygame.MOUSEWHEEL:
            if event.y < 0:
                self.terminal_manager.buffer_index -= 1
                if self.terminal_manager.buffer_index < 0:
                    self.terminal_manager.buffer_index = 0
            else:
                self.terminal_manager.buffer_index += 1
                if self.terminal_manager.buffer_index >= len(
                    self.terminal_manager.buffer
                ):
                    self.terminal_manager.buffer_index = (
                        len(self.terminal_manager.buffer) - 1
                    )

    def update_terminal(
        self,
        rect: tuple[int, int, int, int],
        terminal_manager: TerminalManager,
        signal_flag: bool = False,
        crawler_id: str = "",
    ) -> None:
        """update_terminal

        Updates the Terminal paramters.

        Args:
            rect (tuple[int, int, int, int]): the position and size of the Terminal.
            signal_flag (bool): indicates if there is a signal. Defauls to True.
            crawler_id: (str): Id of the current crawle
        """
        #  Save Terminal parameters.

        self.rect: tuple[int, int, int, int] = rect
        self.terminal_manager: TerminalManager = terminal_manager
        self.signal_flag: bool = signal_flag
        self.crawler_id: str = crawler_id

        #  Update superclass.

        super().update_base(
            rect,
            colour=layout_config.colour,
            corner_radius=layout_config.corner_radius,
            bar=True,
        )

    def render(self, display: pygame.Surface) -> None:
        """render

        Render the Terminal.

        Args:
            display (pygame.event.Event): display on which to render.
        """

        #  Render the Base superclass.

        super().render(display)

        #  Render the Terminal.

        _end: int = 0
        if self.terminal_manager.buffer_index + 8 > len(self.terminal_manager.buffer):
            _end = len(self.terminal_manager.buffer)
        else:
            _end = self.terminal_manager.buffer_index + 8

        _message1: str = f"{self.crawler_id} Terminal"
        if len(self.terminal_manager.buffer) == 0:
            _message2: str = f"No history"
        elif len(self.terminal_manager.buffer) == 1:
            _message2: str = f"1 of 1"
        else:
            _message2: str = (
                f"[{self.terminal_manager.buffer_index+1} to {_end} of {len(self.terminal_manager.buffer)}]"
            )

        show_text(
            display,
            f"{_message1:<15} {_message2:>74}",
            self.base_to_display_rect((0, 0, self.rect[2], 30)),
            layout_config.font,
            BLACK,
            False,
            15,
            9,
        )

        #  Dsiplay message buffer.

        display_terminal_buffer(
            display,
            self.rect,
            self.terminal_manager.buffer,
            self.terminal_manager.buffer_index,
        )

    #  Functions that may be called from functions in the parent class.

    def set_terminal_buffer_index(self, index: int) -> None:
        """set_terminal_buffer_index

        Args:
            index (int): index to set
        """

        if index < 0:
            self.terminal_manager.buffer_index = 0
        elif index >= len(self.terminal_manager.buffer) - 8:
            self.terminal_manager.buffer_index = len(self.terminal_manager.buffer) - 8
        else:
            self.terminal_manager.buffer_index = index
