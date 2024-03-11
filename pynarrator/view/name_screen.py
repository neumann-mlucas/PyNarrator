import pygame
from config import Config
from model import DialogFacade
from view.base import BaseView

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class NameScreenView(BaseView):
    "game start screen class, responsible for rendering the screen and handling mouse events"

    DEFAULT_IMAGE = "start_screen.png"

    def __init__(self, config: Config, model: DialogFacade, screen) -> None:
        super().__init__(config, model, screen)
        self.text = "Enter your name:"
        self.options = []

    def draw_text(self) -> None:
        "draw central text (e.g title or main dialog)"
        # TODO: use a function that wrap lines
        # draw text
        text_render = self.fontTitle.render(self.text, True, WHITE)
        rect = text_render.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2)
        )
        # draw text box
        background_rect = rect.inflate(15, 15)
        pygame.draw.rect(self.screen, BLACK, background_rect)
        # render
        self.screen.blit(text_render, rect)
