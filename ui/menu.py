import pygame
import math

class UIText:
    def __init__(self, text, font, color, y_ratio, blink=False, blink_speed=2):
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


class Menu:
    def __init__(self, window):
        self.window = window

        # Fonts
        self.font = pygame.font.SysFont("mono", 20)
        self.title_font = pygame.font.SysFont("mono", 30)

        # State flags
        self.game_select = False
        self.selected_game = None

        # UI elements
        self.press_space_text = UIText(
            text="Press SPACE to Continue",
            font=self.font,
            color="grey",
            y_ratio=0.5,
            blink=True,
            blink_speed=2
        )

        # Background
        bg_original = pygame.image.load("assets/tabletop.jpg").convert_alpha()
        self.background = pygame.transform.smoothscale(
            bg_original,
            self.window.get_size()
        )

        # Game names for buttons
        self.game_names = ["Baccarat", "Blackjack", "Craps", "Roulette"]
        self.selected_game = None

        # Button parameters
        self.num_buttons = len(self.game_names)
        self.left_margin = 50
        self.right_margin = 50
        self.button_width = 110
        self.button_height = 325
        self.button_y = 50
        self.gap = (self.window.get_width() - self.left_margin - self.right_margin - self.num_buttons * self.button_width) / (self.num_buttons - 1)

        # Generate button Rects
        self.banners = []
        for i in range(self.num_buttons):
            x = self.left_margin + i * (self.button_width + self.gap)
            rect = pygame.Rect(x, self.button_y, self.button_width, self.button_height)
            self.banners.append(rect)

        # Fade-in variables
        self.banner_alpha = 0    # Start fully transparent
        self.fade_speed = 300    # Alpha per second

        # Rounded corner radius and border thickness
        self.corner_radius = 20
        self.border_thickness = 4

    def handle_event(self, event):
        if self.game_select:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, banner in enumerate(self.banners):
                    if banner.collidepoint(mouse_pos):
                        self.selected_game = self.game_names[i].lower()
                        self.game_select = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game_select = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game_select = True

    def update(self, dt):
        # Fade-in banners
        if self.game_select and self.banner_alpha < 255:
            self.banner_alpha += self.fade_speed * (dt / 1000)
            if self.banner_alpha > 255:
                self.banner_alpha = 255

    def draw(self):
        self.window.blit(self.background, (0, 0))

        if not self.game_select:
            # Title card
            title = self.title_font.render("Casino", True, "white")
            title_rect = title.get_rect(
                centerx=self.window.get_width() // 2,
                centery=int(self.window.get_height() * 0.45)
            )
            self.window.blit(title, title_rect)
            self.press_space_text.draw(self.window)
        else:
            # Draw transparent rounded rectangle buttons with yellow border
            for i, banner in enumerate(self.banners):
                # Draw filled rectangle (gray with alpha)
                fill_surf = pygame.Surface((banner.width, banner.height), pygame.SRCALPHA)
                fill_color = (0, 0, 0, int(self.banner_alpha * 0.3))  # semi-transparent
                fill_surf.fill(fill_color)
                self.window.blit(fill_surf, banner.topleft)

                # Draw border (yellow)
                border_surf = pygame.Surface((banner.width, banner.height), pygame.SRCALPHA)
                pygame.draw.rect(
                    border_surf,
                    (255, 200, 0, int(self.banner_alpha)),  # yellow
                    (0, 0, banner.width, banner.height),
                    width=self.border_thickness,
                    border_radius=self.corner_radius
                )
                self.window.blit(border_surf, banner.topleft)

                # Draw game name centered
                label = self.font.render(self.game_names[i], True, (255, 255, 255))
                # Apply alpha
                text_surf = pygame.Surface(label.get_size(), pygame.SRCALPHA)
                text_surf.blit(label, (0, 0))
                text_surf.set_alpha(int(self.banner_alpha))
                text_rect = text_surf.get_rect(center=banner.center)
                self.window.blit(text_surf, text_rect)
