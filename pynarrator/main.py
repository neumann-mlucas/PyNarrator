import pygame
from config import Config
from controller import (GameController, GameState, GameStateGame,
                        GameStateLanguageMenu, GameStateMenu,
                        GameStateNameScreen, LanguageMenuController,
                        MenuController, NameScreenController)
from model import DialogFacade
from view import GameView, LanguageMenuView, MenuView, NameScreenView

CLASS_STATE_MAP = (
    (GameStateMenu, MenuView, MenuController),
    (GameStateLanguageMenu, LanguageMenuView, LanguageMenuController),
    (GameStateNameScreen, NameScreenView, NameScreenController),
    (GameStateGame, GameView, GameController),
)


def init_screen(config: Config):
    pygame.init()
    size = config.width, config.height
    return pygame.display.set_mode(size)


def main():
    "main game loop"

    # Initialize Config
    config = Config()

    # Initialize pygame
    screen = init_screen(config)

    # Initialize dialog model
    model = DialogFacade(config)

    # Initialize components
    controllers = {}
    for state, view_class, controler_class in CLASS_STATE_MAP:
        view = view_class(config, model, screen)
        controller = controler_class(config, model, view)
        controllers[state] = controller

    # Main loop
    running = True
    current_state = GameStateMenu
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break

            # get appropriate controller
            current_controller = controllers[current_state]
            # sync controler state and current_state variable
            current_controller.state = current_state
            # send event to the controller
            current_controller.handle_events(event)
            # update current_state variable state
            current_state = current_controller.state
            # render screen
            current_controller.view.render()

        pygame.display.flip()


if __name__ == "__main__":
    main()
