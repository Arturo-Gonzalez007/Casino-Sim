import pygame
import os


class CardRenderer:

    def __init__(self, window):
        self.window = window
        self.cache = {}

        self.back_original = pygame.image.load(
            os.path.join("assets", "cards", "XcardBack.png")
        ).convert_alpha()

    def get_scaled_size(self):
        width, height = self.window.get_size()

        card_width = int(width * 0.08)
        card_height = int(card_width * 1.45)

        return card_width, card_height

    def get_card_image(self, card):
        key = f"{card.rank}{card.suit}"

        card_width, card_height = self.get_scaled_size()

        if key not in self.cache:
            path = os.path.join("assets", "cards", f"{key}.png")
            original = pygame.image.load(path).convert_alpha()
            self.cache[key] = original

        return pygame.transform.smoothscale(
            self.cache[key],
            (card_width, card_height)
        )

    def get_back_image(self):
        card_width, card_height = self.get_scaled_size()
        return pygame.transform.smoothscale(
            self.back_original,
            (card_width, card_height)
        )

    def draw(self, window, card, position, face_up=True):
        if face_up:
            image = self.get_card_image(card)
        else:
            image = self.get_back_image()

        window.blit(image, position)
