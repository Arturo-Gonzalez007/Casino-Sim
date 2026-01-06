# menu.py
import pygame
from sys import exit


def main():
    game_width = 600
    game_height = 400
    pygame.init()
    window = pygame.display.set_mode((game_width, game_height))
    pygame.display.set_caption("Casino")
    clock = pygame.time.Clock()

    """Game Variables"""
    main_menu = True
    game_paused = False

    font_size = 16
    font = pygame.font.SysFont("mono", font_size)

    def draw_main_menu():
        font = pygame.font.SysFont("mono", 25)
        text = font.render("Casino", True, "white")
        text_rect = text.get_rect(center=pygame.display.get_surface().get_rect().center)
        window.blit(text, text_rect)
    def draw_text(text, text_col, x, y):
        text_surface = font.render(text, True, text_col)
        window.blit(text_surface, (x, y))
        y += font_size + 5
        pygame.display.update()

    while True:
        window.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_menu = False

                    break

        if main_menu:
            draw_main_menu()
            draw_text("Press SPACE to Continue", "Grey", 180, 210)


        pygame.display.update()
        clock.tick(60)
