import pygame

from pathlib import Path
from typing import Callable

from config import Config
from model.dialog import DialogFacade
from view.mixin import ScreenMixin


class DialogScreen(ScreenMixin):
    """
    main game screen class, responsible for:
        - rendering the screen background and text
        - updating screen based on the current dialog state
        - communicating with the dialog graph"
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        # creates dialog graph interface
        self.dialog = DialogFacade(config)
        # initializes screen variables
        self.refresh()

        super().__init__(config)

    def refresh(self) -> None:
        "changes screen variables base on current node of the dialog graph"
        self.background_image_path = str(
            Path(self.config.image_path) / self.dialog.current_img
        )
        self.background_image = pygame.image.load(self.background_image_path)
        self.background_image = pygame.transform.scale(
            self.background_image, (self.config.width, self.config.height)
        )

        self.text = self.dialog.current_text
        self.options = [option.text for option in self.dialog.current_options]
        self.option_labels = [option.label for option in self.dialog.current_options]
        self.options_callbacks = [
            self.chose_nth_option(i) for i, _ in enumerate(self.options)
        ]

    def chose_nth_option(self, n: int) -> Callable:
        "helper function / clousure for advancing the dialog based on a clicked event"

        def chose():
            label = self.option_labels[n]
            self.dialog.next(label)

        return chose

    def dialog_screen(self) -> None:
        "dialog screen game loop"
        while True:
            self.refresh()
            self.screen.blit(self.background_image, (0, 0))
            self.draw_text()
            option_clicked = self.handle_events()
            if option_clicked is not None:
                self.options_callbacks[option_clicked]()
                self.refresh()
            pygame.display.flip()
            self.refresh()
