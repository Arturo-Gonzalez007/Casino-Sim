import random
from collections import deque
from .deck import Deck


class Shoe:
    """
     build shoe
     shuffle shoe
     add shoe to a queue
     deal the cards
     possibly reshuffle after 75% of deck is used"""

    def __init__(self, num_decks = 6, reshuffle_threshold = 0.25):
        self.num_decks = num_decks
        self.reshuffle_threshold = reshuffle_threshold
        self.cards = deque()
        self.build_shoe()
        self.shuffle_shoe()

    def build_shoe(self):
        all_cards = []
        for _ in range(self.num_decks):
            all_cards.extend(Deck.generate_standard_deck())
        self.cards = deque(all_cards)

    def shuffle_shoe(self):
        cards_list = list(self.cards)
        random.shuffle(cards_list)
        self.cards = deque(cards_list)

    def deal_next_card(self):
        if len(self.cards) == 0 or self.needs_reshuffle():
            self.build_shoe()
            self.shuffle_shoe()
        return self.cards.popleft()

    def cards_remaining(self):
        """Return the number of cards left in the shoe."""
        return len(self.cards)

    def needs_reshuffle(self):
        return len(self.cards) <= int(self.num_decks * 52 * self.reshuffle_threshold)
