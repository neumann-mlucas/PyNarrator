from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum

import pygame
from config import Config
from model import DialogFacade
from pygame.event import Event
from view import BaseView


class GameStateEnum(Enum):
    Menu = 1
    Game = 2
    LanguageMenu = 3
    NameScreen = 4


@dataclass
class GameState:
    state: GameStateEnum
    vars: dict[str, str] = field(default_factory=dict)

    def __eq__(self, other) -> bool:
        return self.state == other.state

    def __hash__(self) -> int:
        return hash(self.state)


_vars: dict = defaultdict(lambda: "")

GameStateMenu = GameState(GameStateEnum.Menu, _vars)
GameStateGame = GameState(GameStateEnum.Game, _vars)
GameStateLanguageMenu = GameState(GameStateEnum.LanguageMenu, _vars)
GameStateNameScreen = GameState(GameStateEnum.NameScreen, _vars)


class BaseController:
    """
    a base class for game controllers, providing common functionality and interface
    - attributes "state" and "options_callbacks" need to be set by the children class
    """

    def __init__(self, config: Config, model: DialogFacade, view: BaseView) -> None:
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
