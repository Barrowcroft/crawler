#  The CommandLine class provides a simple interface to the console command lione.

import pygame

import crawler.constants as c
import crawler.customlogger as customlogger
from crawler.config import layout_config
from crawler.console.console_gui_components.base import Base
from crawler.console.console_tools.show_text import show_text


class CommandLine(Base):
    """CommandLine

    he CommandLine class provides a simple interface to the console command lione.

    Args:
        Base (_type_): The CommandLine class subclasses Base.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(self) -> None:
        """__init__

        Initialises the CommandLine class.
        """

        #  Initialise the Base superclass.

        super().__init__()

        #  Initialise the command line.

        self.prompt: str = ""
        self.command_buffer: str = ""

        #  Initialise cursor.

        self.cursor_blink_time: float = 0
        self.cursor_flash_switch: bool = True

    def handleKeyEvent(self, event: pygame.event.Event) -> None:
        """handleKeyEvent

        Handles key events passed to the CommandLine.

        Args:
            event (Event): event to handle
        """
        #  When a key is presssed, if the key press represents a printable
        #  ie, is not Return or Backpace, then if it is alpanumeric or space
        #  add it to the buffer. If the key press is Return then trim the string and return it.
        #  If the key press is backspace then remove the last character from the buffer.
        #  Line length is limited to TERMINAL_LINE_LENGTH (default. 80) characters.

        if event.type == pygame.KEYDOWN:
            if (
                event.key != pygame.K_RETURN
                and event.key != pygame.K_BACKSPACE
                and event.key != pygame.K_UP
                and event.key != pygame.K_DOWN
                and event.key != pygame.K_LEFT
                and event.key != pygame.K_RIGHT
            ):
                if len(self.command_buffer) == c.TERMINAL_LINE_LENGTH:
                    return

                if event.unicode.isalnum():
                    self.command_buffer += pygame.key.name(event.key)
                if event.key == pygame.K_SPACE:
                    self.command_buffer += " "
                if event.key == pygame.K_MINUS:
                    self.command_buffer += "-"

            elif event.key == pygame.K_RETURN:
                self.command_buffer = self.command_buffer.strip()
                self.command_buffer = ""
            elif event.key == pygame.K_BACKSPACE:
                self.command_buffer = self.command_buffer[
                    : len(self.command_buffer) - 1
                ]

    def update_command_line(
        self,
        dt: float,
        rect: tuple[int, int, int, int],
    ):
        """update_command_line

        Args:
            dt (float): delta time.
            rect (tuple[int, int, int, int]): the position and size of the CommandLine.
        """

        #  Adjust the layout of the command line to the bottom of the terminal area.

        self.layout: tuple[int, int, int, int] = (
            rect[0] + 5,
            rect[1] + 185,
            rect[2] - 10,
            30,
        )

        #  Update the timer for the cursor blink_flag.

        self.cursor_blink_time += dt

        #  Update Base superclass.

        super().update_base(self.layout, frame_flag=False)

    def render(self, display: pygame.Surface) -> None:
        """render

        Renders the CommandLine.

        Args:
            display (Surface): display to render on to.
        """

        #  Render the Base superclass.

        super().render(display)

        #  Blink cursor.

        if self.cursor_blink_time > 0.5:
            self.cursor_flash_switch = not self.cursor_flash_switch
            self.cursor_blink_time = 0

        #  Write command line.

        if self.cursor_flash_switch is True:
            show_text(
                display,
                f"{self.prompt}> {self.command_buffer}",
                self.base_to_display_rect((5, 10, self.layout[2], 30)),
                layout_config.font,
                colour=layout_config.colour,
                centered=False,
            )
        else:
            show_text(
                display,
                f"{self.prompt}> {self.command_buffer}_",
                self.base_to_display_rect((5, 10, self.layout[2], 30)),
                layout_config.font,
                colour=layout_config.colour,
                centered=False,
            )

    #  Functions that may be called from functions in the parent class.

    def set_terminal_prompt(self, prompt: str) -> None:
        """set_terminal_prompt

        Args:
            index (int): prompt to set
        """
        self.prompt = prompt

    def set_command_buffer(self, buffer: str) -> None:
        """set_command_buffer

        Args:
            buffer (str): buffer to set
        """
        self.command_buffer = buffer
