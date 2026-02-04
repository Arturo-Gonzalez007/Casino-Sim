import pygame

import core.player
from rng.shoe import Shoe


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
        self.message = "Place your bet (SPACE)"

        self.bet = 10
        self.current_bet = 0
        self.hands_bet = []

        self.all_hands = []
        self.player_hand = []
        self.dealer_hand = []
        self.current_hand = 0
        self.split_active = False

        self.can_double = True
        self.doubled = False
        self.hand_count = 0
        self.player_BJ = False

        self.shoe = Shoe(num_decks=6)

        self.state_start_time = pygame.time.get_ticks()
        self.state_delay = 700

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
                if event.key == pygame.K_UP:
                    if self.current_bet + 10 <= core.player.balance:
                        self.current_bet += 10
                        self.message = f"Bet: ${self.current_bet}"
                elif event.key == pygame.K_DOWN:
                    if self.current_bet >= 10:
                        self.current_bet -= 10
                        self.message = f"Bet: ${self.current_bet}"
                elif event.key == pygame.K_SPACE and self.current_bet > 0:
                    core.player.balance -= self.current_bet
                    self.initial_deal()


            elif self.state == "player_turn":
                if event.key == pygame.K_h:
                    self.player_hit()
                elif event.key == pygame.K_s:
                    self.advance_hand()
                elif event.key == pygame.K_d and self.can_double:
                    self.double_down()
                elif event.key == pygame.K_p and self.can_split():
                    self.split_hand()

            elif self.state == "payout":
                if event.key == pygame.K_SPACE:
                    self.reset_round()

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

        self.all_hands = [self.player_hand]
        self.hand_bets = [self.current_bet]

        self.current_hand = 0
        self.split_active = False
        self.can_double = True
        self.player_BJ = False

        self.set_state("player_turn")
        self.message = "H=Hit S=Stand D=Double P=Split"

        self.check_bj()

    def player_hit(self):
        hand = self.all_hands[self.current_hand]
        hand.append(self.draw_card())
        self.can_double = False

        value = self.hand_value(hand)

        if value >= 21:
            self.advance_hand()

    def advance_hand(self):
        if self.split_active and self.current_hand < len(self.all_hands) - 1:
            self.current_hand += 1
            self.can_double = True
            self.message = f"Playing hand {self.current_hand + 1}"
        else:
            if all(self.hand_value(h) > 21 for h in self.all_hands):
                self.set_state("payout")
                self.game_results()
            else:
                self.set_state("dealer_turn")
                self.message = "Dealer's turn"

    def double_down(self):
        bet = self.hand_bets[self.current_hand]

        if core.player.balance < bet:
            self.message = "Not enough balance to double"
            return

        core.player.balance -= bet
        self.doubled = True
        self.hand_bets[self.current_hand] *= 2

        hand = self.all_hands[self.current_hand]
        hand.append(self.draw_card())
        self.can_double = False

        self.advance_hand()

    def can_split(self):
        hand = self.all_hands[self.current_hand]

        return (
                len(hand) == 2 and
                not self.split_active and
                (
                        hand[0].rank == hand[1].rank or
                        (hand[0].value == 10 and hand[1].value == 10)
                )
        )

    def split_hand(self):
        if core.player.balance < self.current_bet:
            self.message = "Not enough balance to split"
            return

        core.player.balance -= self.current_bet

        card1, card2 = self.player_hand

        self.all_hands = [
            [card1, self.draw_card()],
            [card2, self.draw_card()]
        ]

        self.hand_bets = [self.current_bet, self.current_bet]

        self.split_active = True
        self.current_hand = 0
        self.can_double = True
        self.message = "Playing hand 1"

    def draw_card(self):
        return self.shoe.deal_next_card()

    def update(self, dt):
        now = pygame.time.get_ticks()

        if self.state == "dealer_turn":
            if now - self.state_start_time >= self.state_delay:
                if self.hand_value(self.dealer_hand) < 17:
                    self.dealer_hand.append(self.draw_card())
                    self.set_state("dealer_turn")
                else:
                    self.set_state("payout")
                    self.game_results()

    def check_bj(self):
        player = self.hand_value(self.player_hand)
        dealer = self.hand_value(self.dealer_hand)

        if player == 21:
            self.player_BJ = True
            self.set_state("payout")
            self.game_results()
        elif dealer == 21:
            self.set_state("payout")
            self.message = "Dealer Blackjack"
            self.game_results()

    def game_results(self):
        dealer = self.hand_value(self.dealer_hand)

        for i, hand in enumerate(self.all_hands):
            player = self.hand_value(hand)
            bet = self.hand_bets[i]

            if player > 21:
                continue

            if dealer > 21 or player > dealer:
                win = bet * (1.5 if self.player_BJ else 1)
                core.player.balance += bet + win
                if self.player_BJ:
                    self.message = f"BLACKJACK! YOU WIN +${self.current_bet * 1.5}"
                elif self.doubled:
                    self.message = f"YOU WIN +${self.current_bet *2}"
                elif self.split_active:
                    self.hand_count += 1
                    self.message = f"YOU WIN +${self.current_bet * self.hand_count}"
                else:
                    self.message = f"YOU WIN +${self.current_bet} (SPACE)"
            elif player == dealer:
                core.player.balance += bet
                self.message = "PUSH! (SPACE)"
            else:
                self.message = "YOU LOSE! (SPACE)"


    def reset_round(self):
        self.state = "betting"
        self.message = "Place your bet (SPACE)"
        self.player_hand = []
        self.dealer_hand = []
        self.all_hands = []
        self.current_hand = 0
        self.split_active = False
        self.doubled = False
        self.hand_count = 0

    "Game Rendering"
    def draw(self):
        self.window.blit(self.background, (0, 0))

        lines = [
            "BLACKJACK",
            f"State: {self.state}",
        ]

        if self.split_active:
            for i, hand in enumerate(self.all_hands):
                marker = ">" if i == self.current_hand else " "
                lines.append(
                    f"{marker} Hand {i+1}: {hand} ({self.hand_value(hand)})"
                )
        else:
            lines.append(
                f"Player: {self.player_hand} ({self.hand_value(self.player_hand)})"
            )

        dealer_display = (
            self.dealer_hand
            if self.state != "player_turn"
            else [self.dealer_hand[0], "?"]
        )

        dealer_value = (
            self.hand_value(self.dealer_hand)
            if self.state != "player_turn"
            else self.hand_value([self.dealer_hand[0]])
        )

        lines.append(f"Dealer: {dealer_display} ({dealer_value})")
        lines.append(self.message)
        lines.insert(1, f"Balance: ${core.player.balance}")
        lines.insert(2, f"Bet: ${self.current_bet}")

        y = 50
        for line in lines:
            text = self.font.render(line, True, "white")
            self.window.blit(text, (50, y))
            y += 40

        text = self.font.render("ESC to return", True, "white")
        text_rect = text.get_rect(center=(self.window.get_width() // 2, 350))
        self.window.blit(text, text_rect)
