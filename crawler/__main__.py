#  The main .py file provides the main program entry point; it initilises the game environment and starts the controller.

import pygame  # type: ignore

import crawler.constants as c
import crawler.controller as controller
import crawler.customlogger as customlogger
import crawler.init as init
from crawler.config import layout_config, root_config
from crawler.states.state import State


@customlogger.log_trace(customlogger.Levels.INFO)
def main() -> None:
    """main

    The main program entry.

    (Logging is initialised when the file is executed on inclusion.)
    Sets up/creates the config parser and reads settings.
    Sets the logging level of the custom logger.
    Sets up all the elements of the game engine by calling methods from the init.py file.
    Starts the game controller.

    """
    #  Read the root config file (create it if it doesn't exist).

    root_config.get_config(c.GAME_NAME)

    #  Get the logging level

    _configParser = root_config.root_config
    _logging_level: str = _configParser["logging"]["logging_level"]

    #  Set the logging level.

    customlogger.log_level(_logging_level)

    #  Get the pygame display surface.

    _display: pygame.Surface = init.getDisplay(c.GAME_TITLE)  #  type: ignore

    #  Read the layout config file (create it if it doesn't exist).
    #  This also creates font objects, so must be done after pygame is initialised in getDisplay (above).

    layout_config.get_config()

    #  Get the pygame clock.

    _clock: pygame.time.Clock = init.getClock()  #  type: ignore

    #  Load the game states.

    _gameStates: dict[str, State] = init.getGameStates()

    #  Get the controller and start the game loop.

    _controller: controller.Controller = init.getController(
        _display, _clock, _gameStates, c.INITIAL_STATE
    )
    _controller.run_game()


if __name__ == "__main__":
    main()
