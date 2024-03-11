import json
from pathlib import Path
from typing import Callable

import pygame
from config import Config
from controller.base import (BaseController, GameState, GameStateGame,
                             GameStateNameScreen)
from logger import get_logger
from model import DialogFacade
from pygame.event import Event
from view import GameView

logger = get_logger()


class NameScreenController(BaseController):
    "controller for the game state, handling user interactions during gameplay"

    def __init__(self, config: Config, model: DialogFacade, view: GameView) -> None:
        super().__init__(config, model, view)
        self.state: GameState = GameStateNameScreen
        self.text = ""

    def handle_events(self, event: Event) -> None:
        "handles click events and call the appropriated callback function"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # TODO: capture text o a game state variable
                logger.info(f"User Input: {self.text}")
                self.state.vars["user_name"] = self.text

                self.goto_game()
                self.text = ""  # Clear text after enter
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

            # update shared state
            # TODO: should be done with the GameState obj / enum
            self.view.text = f"Enter your name: {self.text}"

    def update_callbacks(self) -> None:
        "dummy method"
        pass

    def goto_game(self) -> None:
        "enter game"
        self.state = GameStateGame
