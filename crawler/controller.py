#  The contoller handles the main game loop.

from typing import Any

import pygame  # type: ignore

import crawler.eventhandler as eventhandler
from crawler.states.state import State

FPS = 80

import crawler.customlogger as customlogger


class Controller:
    """Controller

    The controller handles the running of the game state loop.
    It is given a starting game state and runs the game loop until the state changes.
    The controller then runs the new game state until another change happens. etc

    The controller calls the event handler to coordinate the handling of user input,
    and calls the current state to update and render itself, before updating the display.
    """

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(
        self,
        display: pygame.Surface,  # type: ignore
        clock: pygame.time.Clock,  # type: ignore
        States: dict[str, Any],
        startingState: str,
    ) -> None:
        """__init__

        Initalises the controller.

        Args:
            display (pygame.event.Event): display on which to render.
            clock (pygame.time.Clock): game clock.
            States (Dict[str, Any]): dictionary of game states.
            startingState (str): starting game state.
        """
        #  Setup surface and clock.

        self._display: pygame.Surface = display  # type: ignore
        self._clock: pygame.time.Clock = clock  # type: ignore

        #  Store game states for later reference.

        self._States: dict[str, Any] = States

        #  Start event handler for current state.

        self._currentState: State = self._States[startingState]()
        self._eventHandler: eventhandler.EventHandler = eventhandler.EventHandler(
            self._currentState
        )

    @customlogger.log_trace(customlogger.Levels.INFO)
    def run_game(self) -> None:
        """run_game

        THIS IS THE MAIN GAME LOOP.

        """
        #  Loop until the game is cancelled.

        while True:
            #  Check to see if state has changed.

            if self._currentState.checkDone():

                #  Clear the display.

                self._display.fill((0, 0, 0, 0))  # type: ignore

                #  Get next state.

                self._currentState = self._States[self._currentState.nextState]()

                #  Update the event handler to handle the new state.

                self._eventHandler.updateState(self._currentState)

            #  Update clock and actual frames per second.

            dt: float = self._clock.tick(FPS) / 1000  # type: ignore
            actualFPS: float = self._clock.get_fps()  # type: ignore

            #  Clear display before render.

            self._display.fill((0, 0, 0))

            #  Handle events, update state and render.

            self._eventHandler.handleEvents()
            self._currentState.update(dt)
            self._currentState.render(self._display, actualFPS)  # type: ignore

            #  Update display.

            pygame.display.flip()  #  type: ignore
