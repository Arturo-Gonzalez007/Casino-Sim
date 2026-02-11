import pygame

import core.player
from rng.shoe import Shoe


class Baccarat:
    BETTING = "betting"
    DEAL = "dealing"
    PLAYER_TURN = "player_turn"
    BANKER_TURN = "banker_turn"
    PAYOUT = "payout"

    def __init__(self, window):
        self.window = window
        self.exit_to_menu = False
        self.font = pygame.font.SysFont("mono", 24)

        # Background
        bg_original = pygame.image.load("assets/tabletop.jpg").convert_alpha()
        self.background = pygame.transform.smoothscale(
            bg_original,
            self.window.get_size()
        )

        # Game data
        self.shoe = Shoe(num_decks=8)
        self.player_hand = []
        self.banker_hand = []
        self.place_bet = None
        self.side_bet = None
        self.current_bet = 0
        self.third_card = False
        self.message = ""

        # State control
        self.state = "betting"
        self.state_start_time = pygame.time.get_ticks()
        self.state_delay = 0

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
                if event.key == pygame.K_UP:
                    if self.current_bet + 10 <= core.player.balance:
                        self.current_bet += 10
                        self.message = f"Bet: ${self.current_bet}"
                elif event.key == pygame.K_DOWN:
                    if self.current_bet >= 10:
                        self.current_bet -= 10
                        self.message = f"Bet: ${self.current_bet}"

                if event.key == pygame.K_p:
                    self.place_bet = "Player"
                    self.message = "Bet on PLAYER"

                elif event.key == pygame.K_b:
                    self.place_bet = "Banker"
                    self.message = "Bet on BANKER"

                if event.key == pygame.K_t:
                    self.side_bet = "Tie"
                    self.message = "Bet on TIE"

                elif event.key == pygame.K_SPACE and self.current_bet > 0 and self.place_bet != None:
                    core.player.balance -= self.current_bet
                    self.set_state("dealing")

            elif self.state == "payout":
                if event.key == pygame.K_SPACE:
                    self.reset_round()

    def update(self, dt):
        now = pygame.time.get_ticks()

        if self.state == "dealing":
            if now - self.state_start_time >= self.state_delay:
                self.initial_deal()
                self.set_state("player_turn")

        elif self.state == self.PLAYER_TURN:
            if now - self.state_start_time >= self.state_delay:
                if self.hand_value(self.player_hand) <= 5:
                    self.player_hand.append(self.draw_card())
                    self.third_card = True
                self.set_state(self.BANKER_TURN, 700)

        elif self.state == "banker_turn":
            if now - self.state_start_time >= self.state_delay:
                self.banker_turn()
                self.set_state("payout")

        elif self.state == "payout":
            if not self.message.startswith("Result"):
                self.game_results()

    """Game Logic"""
    def draw_card(self):
        return self.shoe.deal_next_card()

    def initial_deal(self):
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.banker_hand = [self.draw_card(), self.draw_card()]
        self.third_card = False

    def hand_value(self, hand):
        return sum(card.value for card in hand) % 10

    def banker_turn(self):
        banker_total = self.hand_value(self.banker_hand)

        if self.third_card:
            player_third = self.hand_value([self.player_hand[-1]])
            if banker_total <= 2:
                self.banker_hand.append(self.draw_card())
            elif banker_total == 3 and player_third != 8:
                self.banker_hand.append(self.draw_card())
            elif banker_total == 4 and player_third not in (0, 1, 8, 9):
                self.banker_hand.append(self.draw_card())
            elif banker_total == 5 and 4 <= player_third <= 7:
                self.banker_hand.append(self.draw_card())
            elif banker_total == 6 and 6 <= player_third <= 7:
                self.banker_hand.append(self.draw_card())
        else:
            if banker_total <= 5:
                self.banker_hand.append(self.draw_card())

    def game_results(self):
        player = self.hand_value(self.player_hand)
        banker = self.hand_value(self.banker_hand)

        result = "Tie"
        if player > banker:
            result = "Player"
        elif banker > player:
            result = "Banker"

        if result == self.place_bet:
            self.message = f"Result: {result} — YOU WIN!"
            core.player.balance += self.current_bet*2
        else:
            self.message = f"Result: {result} — YOU LOSE!"

    def reset_round(self):
        self.player_hand.clear()
        self.banker_hand.clear()
        self.place_bet = None
        self.third_card = False
        self.message = ""
        self.set_state("betting")

    """Game Rendering"""
    def draw(self):
        self.window.blit(self.background, (0, 0))

        lines = [
            "BACCARAT",
            f"Balance: {core.player.balance}",
            f"Bet: {self.current_bet}",
            f"Hand: {self.place_bet}",
            f"Player Hand: {self.player_hand} ({self.hand_value(self.player_hand)})",
            f"Banker Hand: {self.banker_hand} ({self.hand_value(self.banker_hand)})",
            self.message,
            "",
            "P = Player | B = Banker",
            "SPACE = Next Round | ESC = Menu"
        ]

        y = 30
        for line in lines:
            text = self.font.render(line, True, "white")
            self.window.blit(text, (40, y))
            y += 32
