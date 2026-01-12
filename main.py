# main.py
import pygame
from ui.menu import Menu


def main():
    pygame.init()

    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Casino")
    clock = pygame.time.Clock()

    # Game states
    MENU = "menu"
    current_state = MENU

    # Create menu
    menu = Menu(screen)

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_state == MENU:
                menu.handle_event(event)

        if current_state == MENU:
            menu.update(dt)
            if menu.start_game:
                current_state = "playing"

        screen.fill("black")
        if current_state == MENU:
            menu.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
