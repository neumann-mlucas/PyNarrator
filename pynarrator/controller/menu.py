import json
import sys
from pathlib import Path

import pygame
from config import Config
from controller.base import (BaseController, GameState, GameStateGame,
                             GameStateLanguageMenu, GameStateMenu,
                             GameStateNameScreen)
from model import DialogFacade
from view import MenuView


class MenuController(BaseController):
    "controller for the main menu, handling user interactions within the menu"

    def __init__(self, config: Config, model: DialogFacade, view: MenuView) -> None:
        super().__init__(config, model, view)
        self.state: GameState = GameStateMenu

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
        self.state = GameStateNameScreen

    def load_game(self) -> None:
        "loads save game"
        self.state = GameStateGame

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
        self.state = GameStateLanguageMenu

    def exit(self) -> None:
        "exits game"
        pygame.quit()
        sys.exit()
