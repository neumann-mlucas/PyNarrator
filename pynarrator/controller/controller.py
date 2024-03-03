import sys
import pygame
import json

from enum import Enum
from pathlib import Path
from typing import Callable

from pygame.event import Event

from config import Config
from model.dialog import DialogFacade
from view.game import GameView
from view.menu import MenuView


class GameState(Enum):
    Menu = 1
    Game = 2
    LanguageMenu = 3


class BaseController:
    """
    a base class for game controllers, providing common functionality and interface
    - attributes "state" and "options_callbacks" need to be set by the children class
    """

    def __init__(self, config: Config, model: DialogFacade, view: MenuView) -> None:
        self.config = config
        self.model = model
        self.view = view
        self.update_callbacks()

    def update_callbacks(self) -> None:
        "sets up callbacks for handling events. should be overridden in subclasses"
        pass

    def handle_events(self, event: Event) -> None:
        "handles click events and call the appropriated callback function"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for i, rect in enumerate(self.view.option_rects):
                if rect.collidepoint(mouse_pos):
                    self.options_callbacks[i]()
                    self.update_callbacks()


class MenuController(BaseController):
    "controller for the main menu, handling user interactions within the menu"

    def __init__(self, config: Config, model: DialogFacade, view: MenuView) -> None:
        super().__init__(config, model, view)
        self.state: GameState = GameState.Menu

    def update_callbacks(self) -> None:
        "start, load and exit menu button callbacks"
        self.options_callbacks = [
            self.start_game,
            self.load_game,
            self.chose_language,
            self.exit,
        ]

    def start_game(self) -> None:
        "change game state"
        self.model.reset()
        self.state = GameState.Game

    def load_game(self) -> None:
        "loads save game"
        self.state = GameState.Game

        # check if save game exists
        path = Path(self.config.save_path) / "save.json"
        if not path.exists():
            return

        # load save
        with open(path, "r") as fp:
            history = json.load(fp)

        # advance game state using history
        self.model.load(history)

    def chose_language(self) -> None:
        "goto language menu"
        self.state = GameState.LanguageMenu

    def exit(self) -> None:
        "exits game"
        pygame.quit()
        sys.exit()


class LanguageMenuController(BaseController):
    "controller for the main menu, handling user interactions within the menu"

    def __init__(self, config: Config, model: DialogFacade, view: MenuView) -> None:
        super().__init__(config, model, view)
        self.state: GameState = GameState.LanguageMenu

    def update_callbacks(self):
        "sets up callbacks for each languages in the menu"
        self.options_callbacks = [
            self.chose_language(i) for i, _ in enumerate(self.config.languages)
        ] + [self.goto_menu]

    def chose_language(self, n: int) -> Callable:
        "helper function / clousure for choosing a language based on a clicked event"

        def chose():
            lang = self.config.languages[n]
            self.config.language = lang
            self.model.reload_config(self.config)
            # go to menu after choosing
            self.state: GameState = GameState.Menu

        return chose

    def goto_menu(self):
        "save game state and go to menu"
        self.state = GameState.Menu


class GameController(BaseController):
    "controller for the game state, handling user interactions during gameplay"

    def __init__(self, config: Config, model: DialogFacade, view: GameView) -> None:
        super().__init__(config, model, view)
        self.state: GameState = GameState.Game

    def update_callbacks(self):
        "sets up callbacks for each dialog option in the game view"
        self.options_callbacks = [
            self.chose_nth_option(i) for i, _ in enumerate(self.model.current_options)
        ]
        self.options_callbacks.append(self.goto_menu)

    def chose_nth_option(self, n: int) -> Callable:
        "helper function / clousure for advancing the dialog based on a clicked event"

        def chose():
            label = self.view.option_labels[n]
            self.model.next(label)

        return chose

    def goto_menu(self):
        "save game state and go to menu"
        history = self.model.history
        self.save_game(history)
        self.state = GameState.Menu

    def save_game(self, history: list[str]) -> None:
        "save game state as a history if the nodes visited"
        path = Path(self.config.save_path) / "save.json"
        with open(path, "w") as fp:
            json.dump(history, fp)
