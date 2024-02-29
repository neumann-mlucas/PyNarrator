import sys
import pygame

from enum import Enum
from typing import Callable

from pygame.event import Event

from model.dialog import DialogFacade
from view.menu import MenuView
from view.game import GameView


class GameState(Enum):
    Menu = 1
    Game = 2


class BaseController:
    "a base class for game controllers, providing common functionality and interface"

    def __init__(self, model: DialogFacade, view: MenuView) -> None:
        self.model = model
        self.view = view
        self.update_callbacks()

    @property
    def state(self) -> None:
        "returns game state, used to change screens in game"
        return self._state

    def update_callbacks(self) -> None:
        "sets up callbacks for handling events. should be overridden in subclasses"
        pass

    def handle_events(self, event: Event) -> None:
        "handles click events and call the appropriated callback function"
        print(type(event), event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for i, rect in enumerate(self.view.option_rects):
                if rect.collidepoint(mouse_pos):
                    self.options_callbacks[i]()
                    self.update_callbacks()


class MenuController(BaseController):
    "controller for the main menu, handling user interactions within the menu"

    def __init__(self, model: DialogFacade, view: MenuView) -> None:
        super().__init__(model, view)
        self._state = GameState.Menu

    def update_callbacks(self) -> None:
        "start, load and exit menu button callbacks"
        self.options_callbacks = [self.start_game, self.load_game, self.exit]

    def start_game(self) -> None:
        "change game state"
        print(self._state)
        self._state = GameState.Game

    def load_game(self) -> None:
        "loads save game"
        pass

    def exit(self) -> None:
        "exits game"
        pygame.quit()
        sys.exit()


class GameController(BaseController):
    "controller for the game state, handling user interactions during gameplay"

    def __init__(self, model: DialogFacade, view: GameView) -> None:
        super().__init__(model, view)
        self._state = GameState.Game

    def update_callbacks(self):
        "sets up callbacks for each dialog option in the game view"
        self.options_callbacks = [
            self.chose_nth_option(i) for i, _ in enumerate(self.model.current_options)
        ]

    def chose_nth_option(self, n: int) -> Callable:
        "helper function / clousure for advancing the dialog based on a clicked event"

        def chose():
            label = self.view.option_labels[n]
            self.model.next(label)

        return chose
