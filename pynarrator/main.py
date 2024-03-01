import pygame

from config import Config
from controller.controller import GameController, MenuController, GameState

from model.dialog import DialogFacade
from view.game import GameView
from view.menu import MenuView


def init_screen(config: Config):
    pygame.init()
    size = config.width, config.height
    return pygame.display.set_mode(size)


def main():
    "main game loop"

    # Initialize Config
    # TODO: parse config options from somewhere
    config = Config()

    # Initialize pygame
    screen = init_screen(config)

    # Initialize dialog model
    model = DialogFacade(config)

    # Initialize components
    menu_view = MenuView(config, model, screen)
    menu_controller = MenuController(config, model, menu_view)

    game_view = GameView(config, model, screen)
    game_controller = GameController(config, model, game_view)

    # Main loop
    running = True
    current_state = GameState.Menu
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break
            elif current_state == GameState.Menu:
                controller = menu_controller
            elif current_state == GameState.Game:
                controller = game_controller

            # sync controler state and current_state variable
            controller.state = current_state
            # send event to the controller
            controller.handle_events(event)
            # update current_state variable state
            current_state = controller.state
            # render screen
            controller.view.render()

        pygame.display.flip()


if __name__ == "__main__":
    main()
