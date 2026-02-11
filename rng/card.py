class Card:
    """Represents a single playing card with rank and suit."""

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    @property
    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def __str__(self):
        return f"{self.rank}{self.suit}"
