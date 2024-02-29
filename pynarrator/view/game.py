import pygame

from pathlib import Path

from config import Config
from model.dialog import DialogFacade
from view.base import BaseView


class GameView(BaseView):
    """
    main game screen class, responsible for:
        - rendering the screen background and text
        - updating screen based on the current dialog state
    """

    DEFAULT_IMAGE = "waiter.png"

    def __init__(self, config: Config, model: DialogFacade, screen) -> None:
        super().__init__(config, model, screen)
        self.update_text()

    def update_text(self) -> None:
        "changes screen variables base on current node of the dialog graph"
        self.background_image_path = str(
            Path(self.config.image_path) / self.model.current_img
        )
        self.background_image = pygame.image.load(self.background_image_path)
        self.background_image = pygame.transform.scale(
            self.background_image, (self.config.width, self.config.height)
        )

        self.text = self.model.current_text
        self.options = [option.text for option in self.model.current_options]
        self.option_labels = [option.label for option in self.model.current_options]
