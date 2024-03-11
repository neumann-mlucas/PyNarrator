import json
from pathlib import Path
from typing import Callable

from config import Config
from controller.base import (BaseController, GameState, GameStateGame,
                             GameStateMenu)
from model import DialogFacade
from view import GameView


class GameController(BaseController):
    "controller for the game state, handling user interactions during gameplay"

    def __init__(self, config: Config, model: DialogFacade, view: GameView) -> None:
        super().__init__(config, model, view)
        self.state: GameState = GameStateGame

    def update_callbacks(self) -> None:
        "sets up callbacks for each dialog option in the game view"
        self.options_callbacks = [
            self.chose_nth_option(i) for i, _ in enumerate(self.model.current_options)
        ]
        self.options_callbacks.append(self.goto_menu)

    def chose_nth_option(self, n: int) -> Callable:
        "helper function / clousure for advancing the dialog based on a clicked event"

        def chose() -> None:
            label = self.view.option_labels[n]
            self.model.next(label)

        return chose

    def goto_menu(self) -> None:
        "save game state and go to menu"
        history = list(self.model.history)
        self.save_game(history)
        self.state = GameStateMenu

    def save_game(self, history: list[str]) -> None:
        "save game state as a history if the nodes visited"
        path = Path(self.config.save_path) / "save.json"
        with open(path, "w") as fp:
            json.dump(history, fp)
