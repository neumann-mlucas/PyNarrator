from typing import Callable

from config import Config
from controller.base import (BaseController, GameState, GameStateLanguageMenu,
                             GameStateMenu)
from model import DialogFacade
from view import LanguageMenuView


class LanguageMenuController(BaseController):
    "controller for the main menu, handling user interactions within the menu"

    def __init__(
        self, config: Config, model: DialogFacade, view: LanguageMenuView
    ) -> None:
        super().__init__(config, model, view)
        self.state: GameState = GameStateLanguageMenu

    def update_callbacks(self) -> None:
        "sets up callbacks for each languages in the menu"
        self.options_callbacks = [
            self.chose_language(i) for i, _ in enumerate(self.config.languages)
        ]

    def chose_language(self, n: int) -> Callable:
        "helper function / clousure for choosing a language based on a clicked event"

        def chose():
            lang = self.config.languages[n]
            self.config.language = lang
            self.model.reload_config(self.config)
            # go to menu after choosing
            self.state: GameState = GameStateMenu

        return chose

    def goto_menu(self) -> None:
        "save game state and go to menu"
        self.state = GameStateMenu
