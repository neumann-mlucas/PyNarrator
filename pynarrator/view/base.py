from pathlib import Path

import pygame
from config import Config
from model import DialogFacade

# Colors
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

FONT_BIG = pygame.font.Font(None, 28)
FONT_MEDIUM = pygame.font.Font(None, 24)


class BaseView:
    "a base class for game views / game scrrens, providing common functionality and interface"

    DEFAULT_IMAGE = "start_screen.png"

    def __init__(self, config: Config, model: DialogFacade, screen) -> None:
        self.config = config
        self.model = model
        self.screen = screen

        # initialize screen variables
        self.background_image_path = str(Path(config.image_path) / self.DEFAULT_IMAGE)
        self.fontTitle = FONT_BIG
        self.font = FONT_MEDIUM

        # set background
        self.screen_width, self.screen_height = config.width, config.height
        self.background_image = pygame.image.load(self.background_image_path)
        self.background_image = pygame.transform.scale(
            self.background_image, (self.screen_width, self.screen_height)
        )
        # clickable rectangles
        self.option_rects: list = []

        # defaults
        self.text = ""
        self.options: list = []

    def update_text(self) -> None:
        "changes screen variables base on game state"
        pass

    def draw_text(self) -> None:
        "draw central text (e.g title or main dialog)"
        # TODO: use a function that wrap lines
        # draw text
        text_render = self.fontTitle.render(self.text, True, WHITE)
        rect = text_render.get_rect(center=(self.screen_width / 2, 50))
        # draw text box
        background_rect = rect.inflate(15, 15)
        pygame.draw.rect(self.screen, BLACK, background_rect)
        # render
        self.screen.blit(text_render, rect)

    def draw_choises(self, text: str, position: tuple[int, int]):
        "draw clickable options in the game screen"
        # draw text
        text_render = self.font.render(text, True, WHITE)
        rect = text_render.get_rect(center=position)
        # draw text box
        background_rect = rect.inflate(10, 10)
        pygame.draw.rect(self.screen, BLACK, background_rect)
        # render
        self.screen.blit(text_render, rect)
        return rect

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
