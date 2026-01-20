import pygame
from rng.shoe import Shoe
from core.player import balance


class Blackjack:

    BETTING = "betting"
    PLAYER = "player_turn"
    DEALER = "dealer_turn"
    PAYOUT = "payout"

    def __init__(self, window):
        self.window = window
        self.exit_to_menu = False
        self.font = pygame.font.SysFont("mono", 24)

        self.state = "betting"
        self.message = "place your bet"

        self.player_balance = balance
        self.bet = 10
        self.player_hand = []
        self.dealer_hand = []
        self.can_double = True
        self.player_BJ = False
        self.shoe = Shoe(num_decks=6)

        self.state_start_time = pygame.time.get_ticks()
        self.state_delay = 700

        # Background
        bg_original = pygame.image.load("assets/tabletop.jpg").convert_alpha()
        self.background = pygame.transform.smoothscale(
            bg_original,
            self.window.get_size()
        )

    def set_state(self, new_state, delay=700):
        self.state = new_state
        self.state_delay = delay
        self.state_start_time = pygame.time.get_ticks()

    """Input Handling"""
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.exit_to_menu = True

            if self.state == "betting":
                if event.key == pygame.K_SPACE:
                    self.initial_deal()

            elif self.state == "player_turn":
                if event.key == pygame.K_h:
                    self.player_hit()
                elif event.key == pygame.K_s:
                    self.set_state("dealer_turn")
                    self.message = "Dealer's turn"
                elif event.key == pygame.K_d and self.can_double:
                    self.double_down()

            elif self.state == "payout":
                if event.key == pygame.K_SPACE:
                    self.state = "betting"
                    self.player_hand = []
                    self.dealer_hand = []
                    self.message = "Place your bet"

    """Game Logic"""

    def hand_value(self, hand):
        total = sum(card.value for card in hand)
        aces = sum(1 for card in hand if card.rank == 'A')

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    def initial_deal(self):
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]
        self.can_double = True
        self.player_BJ = False
        self.set_state("player_turn")
        self.message = "H=Hit D=Double S=Stand"
        self.check_bj()

    def player_hit(self):
        self.player_hand.append(self.draw_card())
        self.can_double = False

        if self.hand_value(self.player_hand) > 21:
            self.set_state("payout")
            self.message = "You Bust!"

    def double_down(self):
        self.bet *= 2
        self.player_hand.append(self.draw_card())
        self.can_double = False
        self.set_state("dealer_turn")
        self.message = "Doubled Down!"

    def draw_card(self):
        return self.shoe.deal_next_card()

    def update(self, dt):
        now = pygame.time.get_ticks()

        if self.state == "dealer_turn":
            if now - self.state_start_time >= self.state_delay:
                if self.hand_value(self.dealer_hand) < 17:
                    self.dealer_hand.append(self.draw_card())
                    self.set_state("dealer_turn", 700)
                else:
                    self.set_state("payout", 700)
                    self.game_results()

    def check_bj(self):
        player = self.hand_value(self.player_hand)
        dealer = self.hand_value(self.dealer_hand)
        if player == 21:
            self.player_BJ = True
            self.set_state("payout")
            self.message = "BLACKJACK!"
        elif dealer == 21:
            self.set_state("payout")
            self.message = "Dealer Blackjack, YOU LOSE"

    def game_results(self):
        player = self.hand_value(self.player_hand)
        dealer = self.hand_value(self.dealer_hand)
        winnings = self.bet

        if player > 21:
            self.message = "You Bust!"
            self.player_balance -= self.bet

        elif dealer > 21 or player > dealer:
            if self.player_BJ:
                winnings *= 1.5
                self.message = "BLACKJACK! YOU WIN!"
            else:
                self.message = "YOU WIN!"
            self.player_balance += winnings

        elif player < dealer:
            self.message = "DEALER WIN!"
            self.player_balance -= self.bet

        else:
            self.message = "PUSH!"

    "Game Rendering"
    def draw(self):
        self.window.blit(self.background, (0, 0))

        lines = [
            "BLACKJACK",
            f"State: {self.state}",
            f"Player: {self.player_hand} ({self.hand_value(self.player_hand)})",
            f"Dealer: {self.dealer_hand if self.state != 'player_turn' else [self.dealer_hand[0], '?']} "
            f"({self.hand_value(self.dealer_hand) if self.state != 'player_turn' else self.hand_value([self.dealer_hand[0]])})",
            self.message,
        ]

        y = 50
        for line in lines:
            text = self.font.render(line, True, "white")
            self.window.blit(text, (50, y))
            y += 40

        text = self.font.render("ESC to return", True, "white")
        text_rect = text.get_rect(center=(self.window.get_width()//2, 350))
        self.window.blit(text, text_rect)
