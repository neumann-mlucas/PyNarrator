import pygame
import sys

from pathlib import Path

from view.mixin import ScreenMixin
from view.dialog import DialogScreen
from config import Config


class StartScreen(ScreenMixin):
    "game start screen class, responsible for rendering the screen and handling mouse events"

    def __init__(self, config: Config) -> None:
        self.config = config

        # initialize screen variables
        self.background_image_path = str(Path(config.image_path) / "start_screen.png")
        self.text = "TEST GAME"
        self.options = ["Start Game", "Load Game", "Exit"]
        self.options_callbacks = [self.start_game, self.load_game, self.exit]

        # TODO: review how to call another screen here
        self.game = DialogScreen(self.config)

        super().__init__(config)

    def main_screen(self):
        "start screen game loop"
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.draw_text()
            option_clicked = self.handle_events()
            if option_clicked is not None:
                self.options_callbacks[option_clicked]()
            pygame.display.flip()

    def start_game(self) -> None:
        "calls game screen"
        self.game.dialog_screen()

    def load_game(self) -> None:
        "loads save game"
        pass

    def exit(self) -> None:
        "exits game"
        pygame.quit()
        sys.exit()


def main():
    view = StartScreen(Config())
    view.main_screen()


if __name__ == "__main__":
    main()
