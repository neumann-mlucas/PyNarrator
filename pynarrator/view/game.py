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

    def render(self) -> None:
        "draws all text the is display in the screen"
        self.screen.blit(self.background_image, (0, 0))

        self.update_text()
        self.draw_text()

        # created clickable rectangles in a loop
        self.option_rects.clear()
        for i, option in enumerate(self.options):
            rect = self.draw_choises(option, (int(self.screen_width / 2), 250 + i * 50))
            self.option_rects.append(rect)

        rect = self.draw_choises(
            "Back to Main Menu", (int(self.screen_width / 2), self.screen_height - 50)
        )
        self.option_rects.append(rect)
