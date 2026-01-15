# main.py
import pygame
from ui.menu import Menu
from games.blackjack import Blackjack
from games.baccarat import Baccarat



def main():
    pygame.init()

    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Casino")
    clock = pygame.time.Clock()

    # Game states
    MENU = "menu"
    BACCARAT = "baccarat"
    BLACKJACK = "blackjack"
    CRAPS = "craps"
    ROULETTE = "roulette"
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

            elif current_state == BLACKJACK:
                blackjack.handle_event(event)

            elif current_state == BACCARAT:
                baccarat.handle_event(event)

        """UPDATE"""

        if current_state == MENU:
            menu.update(dt)

            if menu.selected_game == "blackjack":
                blackjack = Blackjack(screen)
                current_state = BLACKJACK
                menu.selected_game = None

            elif menu.selected_game == "baccarat":
                baccarat = Baccarat(screen)
                current_state = BACCARAT
                menu.selected_game = None

        elif current_state == BLACKJACK:
            blackjack.update(dt)

            if blackjack.exit_to_menu:
                current_state = MENU
                blackjack = None

        elif current_state == BACCARAT:
            baccarat.update(dt)

            if baccarat.exit_to_menu:
                current_state = MENU
                baccarat = None

        screen.fill("black")
        if current_state == MENU:
            menu.draw()

        elif current_state == BLACKJACK:
            blackjack.draw()

        elif current_state == BACCARAT:
            baccarat.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
