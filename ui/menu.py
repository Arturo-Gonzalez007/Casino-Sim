import pygame
from sys import exit
import math

class UIText:
    def __init__(
        self,
        text,
        font,
        color,
        y_ratio,
        blink=False,
        blink_speed=2
    ):
        self.text = text
        self.font = font
        self.color = color
        self.y_ratio = y_ratio
        self.blink = blink
        self.blink_speed = blink_speed

    def draw(self, window):
        text_surface = self.font.render(self.text, True, self.color)

        if self.blink:
            time = pygame.time.get_ticks() / 1000
            alpha = int((math.sin(time * self.blink_speed) + 1) / 2 * 255)
            text_surface.set_alpha(alpha)

        text_rect = text_surface.get_rect(
            centerx=window.get_width() // 2,
            centery=int(window.get_height() * self.y_ratio)
        )

        window.blit(text_surface, text_rect)


def draw_text_centered(window, font, text, color, y_ratio):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(
        centerx=window.get_width() // 2,
        centery=int(window.get_height() * y_ratio)
    )
    window.blit(text_surface, text_rect)


def main():
    pygame.init()

    game_width = 600
    game_height = 400

    window = pygame.display.set_mode((game_width, game_height))
    pygame.display.set_caption("Casino")
    clock = pygame.time.Clock()

    main_menu = True

    '''Font Settings'''
    base_font_size = 16
    font = pygame.font.SysFont("mono", base_font_size)
    title_font_size = 30
    title_font = pygame.font.SysFont("mono", title_font_size)

    press_space_text = UIText(
        text="Press SPACE to Continue",
        font=font,
        color="grey",
        y_ratio=0.5,
        blink=True,
        blink_speed = 2
    )

    """Background Settings"""
    background_original = pygame.image.load('assets/tabletop.jpg').convert_alpha()
    background_resolution = (game_width, game_height)
    background = pygame.transform.smoothscale(background_original, background_resolution)

    while True:
        window.fill("black")
        # Background image
        window.blit(background, (0 , 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_menu = False

        if main_menu:
            draw_text_centered(window, title_font, "Casino", "white", 0.45)
            press_space_text.draw(window)

        pygame.display.update()
        clock.tick(60)


main()
