from .card import Card


class Deck:
    """Represents a standard 52-card deck as a template."""

    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['♠', '♥', '♦', '♣']  # Spades, Hearts, Diamonds, Clubs

    @classmethod
    def generate_standard_deck(cls):
        """Return a list of Card objects representing a standard deck."""
        deck = []
        for suit in cls.suits:
            for rank in cls.ranks:
                deck.append(Card(rank, suit))
        return deck
