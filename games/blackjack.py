import pygame

import core.player
from rng.shoe import Shoe
from ui.card_renderer import CardRenderer


class Blackjack:

    BETTING = "betting"
    PLAYER = "player_turn"
    DEALER = "dealer_turn"
    PAYOUT = "payout"

    def __init__(self, window):
        self.window = window
        self.exit_to_menu = False
        self.font = pygame.font.SysFont("mono", 24)
        self.card_renderer = CardRenderer(self.window)

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

        self.state = "betting"
        self.message = f"Place your bet ${self.current_bet} (SPACE)"

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
                        self.message = f"Place your bet ${self.current_bet} (SPACE)"
                elif event.key == pygame.K_DOWN:
                    if self.current_bet >= 10:
                        self.current_bet -= 10
                        self.message = f"Place your bet ${self.current_bet} (SPACE)"
                elif event.key == pygame.K_SPACE and 0 < self.current_bet <= core.player.balance:
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

        self.update_buttons()

        self.check_bj()

    def update_buttons(self):
        options = ["H=Hit", "S=Stand"]

        if self.can_double:
            options.append("D=Double")

        if self.can_split():
            options.append("P=Split")

        self.message = " ".join(options)

    def player_hit(self):
        hand = self.all_hands[self.current_hand]
        hand.append(self.draw_card())
        self.can_double = False
        self.update_buttons()

        value = self.hand_value(hand)

        if value >= 21:
            self.advance_hand()

    def advance_hand(self):
        if self.split_active and self.current_hand < len(self.all_hands) - 1:
            self.current_hand += 1
            self.can_double = True
            self.update_buttons()
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
        self.update_buttons()

        self.advance_hand()

    def can_split(self):
        hand = self.all_hands[self.current_hand]

        if len(hand) == 2 and (hand[0].rank == hand[1].rank or (hand[0].value == 10 and hand[1].value == 10)):
            return True

    def split_hand(self):

        if core.player.balance < self.current_bet:
            self.message = "Not enough balance to split"
            return

        # limit to 4 total hands
        if len(self.all_hands) >= 4:
            self.message = "Maximum splits reached"
            return

        core.player.balance -= self.current_bet

        hand = self.all_hands[self.current_hand]
        card1, card2 = hand

        # create two new hands
        new_hand1 = [card1, self.draw_card()]
        new_hand2 = [card2, self.draw_card()]

        # replace current hand with first new hand
        self.all_hands[self.current_hand] = new_hand1

        # insert second new hand right after it
        self.all_hands.insert(self.current_hand + 1, new_hand2)

        # duplicate bet for the new hand
        self.hand_bets.insert(self.current_hand + 1, self.current_bet)

        self.split_active = True
        self.can_double = True
        self.update_buttons()

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
                    self.message = f"BLACKJACK! YOU WIN +${self.current_bet * 1.5:.0f}"
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
        self.message = f"Place your bet ${self.current_bet} (SPACE)"
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

        width, height = self.window.get_size()

        margin_x = int(width * 0.05)
        margin_y = int(height * 0.05)

        spacing = int(width * 0.06)

        y = margin_y

        # Title
        title = self.font.render("BLACKJACK", True, "white")
        self.window.blit(title, (margin_x, y))
        y += int(height * 0.06)

        # Balance + Bet
        balance_text = self.font.render(f"Balance: ${core.player.balance:.0f}", True, "white")
        self.window.blit(balance_text, (margin_x, y))
        y += int(height * 0.04)

        # Dealer cards
        dealer_y = int(height * 0.12)
        card_width, _ = self.card_renderer.get_scaled_size()

        dealer_hand_width = card_width + (len(self.dealer_hand) - 1) * spacing
        dealer_x = (width - dealer_hand_width) // 2

        for i, card in enumerate(self.dealer_hand):
            if i == 1 and self.state == "player_turn":
                self.card_renderer.draw(self.window, card, (dealer_x, dealer_y), face_up=False)
            else:
                self.card_renderer.draw(self.window, card, (dealer_x, dealer_y), face_up=True)

            dealer_x += spacing

        if self.state != "player_turn":
            dealer_value = self.hand_value(self.dealer_hand)
        else:
            dealer_value = self.hand_value([self.dealer_hand[0]])

        dealer_text = self.font.render(f"Dealer: {dealer_value}", True, "white")
        self.window.blit(dealer_text, (margin_x, int(height * 0.18)))

        # Player / Split hands
        start_y = int(height * 0.55)

        if self.split_active:
            start_y = int(self.window.get_height() * 0.55)

            if self.split_active:
                num_hands = len(self.all_hands)
                max_columns = 4
                column_width = self.window.get_width() // max_columns

                for i, hand in enumerate(self.all_hands):

                    center_x = column_width * i + column_width // 2
                    y = start_y

                    # draw stacked cards
                    for j, card in enumerate(hand):
                        x = center_x - 40 + j * 30  # 30px overlap stack
                        self.card_renderer.draw(self.window, card, (x, y), face_up=True)

                    # draw value
                    value_text = self.font.render(
                        f"{self.hand_value(hand)}",
                        True,
                        "white"
                    )
                    self.window.blit(value_text, (center_x - 20, y - 30))

                    # active hand marker
                    if i == self.current_hand and self.state == "player_turn":
                        marker = self.font.render("▼", True, "yellow")
                        self.window.blit(marker, (center_x - 10, y - 60))

        else:
            hand = self.player_hand

            hand_width = card_width + (len(hand) - 1) * spacing
            x = (width - hand_width) // 2
            y = start_y

            for card in hand:
                self.card_renderer.draw(self.window, card, (x, y), face_up=True)
                x += spacing

            value_text = self.font.render(
                f"Player: {self.hand_value(self.player_hand)}",
                True,
                "white"
            )
            self.window.blit(value_text, (margin_x, y + int(height * 0.02)))

        # Message
        message_text = self.font.render(self.message, True, "white")
        self.window.blit(message_text, (margin_x, int(height * 0.85)))

        # ESC text
        esc_text = self.font.render("ESC to return", True, "white")
        esc_rect = esc_text.get_rect(center=(width // 2, int(height * 0.95)))
        self.window.blit(esc_text, esc_rect)


