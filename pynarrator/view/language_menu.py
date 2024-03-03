from config import Config
from model import DialogFacade
from view.base import BaseView


class LanguageMenuView(BaseView):
    "game start screen class, responsible for rendering the screen and handling mouse events"

    DEFAULT_IMAGE = "start_screen.png"

    def __init__(self, config: Config, model: DialogFacade, screen) -> None:
        super().__init__(config, model, screen)
        self.text = "CHOOSE A LANGUAGE"
        self.options = list(config.languages)
