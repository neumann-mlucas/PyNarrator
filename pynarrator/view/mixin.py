import pygame
import sys

from config import Config


# Colors
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

FONT_BIG = pygame.font.Font(None, 30)
FONT_MEDIUM = pygame.font.Font(None, 24)


class ScreenMixin:
    "implements screen render functions that are common between the start screen and the game screen"

    def __init__(self, config: Config) -> None:
        # initialize screen
        self.screen_width = config.width
        self.screen_height = config.height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # set fonts
        self.fontTitle = FONT_BIG
        self.font = FONT_MEDIUM

        # set background
        self.background_image = pygame.image.load(self.background_image_path)
        self.background_image = pygame.transform.scale(
            self.background_image, (self.screen_width, self.screen_height)
        )

        # clickable rectangles
        self.option_rects: list = []

        # validate class initialization
        self.validate_attrs()

    def validate_attrs(self) -> None:
        "checks if class has all the necessary attriubutes"
        has_all_attrs = (
            hasattr(self, "background_image_path")
            and hasattr(self, "text")
            and hasattr(self, "options")
            and hasattr(self, "options_callbacks")
        )
        has_all_callbacks = len(self.options) == len(self.options_callbacks)
        assert (
            has_all_attrs and has_all_callbacks
        ), "Class was not initialized correctly"

    def draw_main_text(self) -> None:
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

    def draw_text(self) -> None:
        "draws all text the is display in the screen"
        self.draw_main_text()
        self.option_rects.clear()
        # created clickable rectangles in a loop
        for i, option in enumerate(self.options):
            rect = self.draw_choises(option, (int(self.screen_width / 2), 250 + i * 50))
            self.option_rects.append(rect)

    def handle_events(self) -> int | None:
        "handles click events and call the appropriated callback function"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        return i
