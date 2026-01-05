from core.player import adjust_balance, show_balance
from rng.shoe import Shoe

# Initialize the shoe with 6 decks
shoe = Shoe(num_decks=6)

def calculate_hand(hand):
    """Calculate the total value of a blackjack hand, adjusting Aces as needed."""
    total = sum(card.value for card in hand)
    aces = sum(1 for card in hand if card.rank == 'A')
    while total > 21 and aces:
        total -= 10  # treat Ace as 1 instead of 11
        aces -= 1
    return total

def display_hand(hand):
    """Return a string representation of a hand."""
    return ', '.join(str(card) for card in hand)

def play_round():
    """Play a single round of blackjack."""
    print(f"\nCurrent balance: ${show_balance()}")

    # Ask for bet
    while True:
        try:
            bet = int(input("Enter your bet amount: "))
            if bet <= 0:
                print("Bet must be greater than 0.")
            elif bet > show_balance():
                print("Not enough balance to bet that amount.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    # Place bet
    adjust_balance(-bet)
    print(f"You bet ${bet}. Balance now: ${show_balance()}")

    # Deal initial hands
    player_hand = [shoe.deal_next_card(), shoe.deal_next_card()]
    dealer_hand = [shoe.deal_next_card(), shoe.deal_next_card()]

    print(f"Your hand: {display_hand(player_hand)} -> total {calculate_hand(player_hand)}")
    print(f"Dealer shows: [{dealer_hand[0]}, ?]")

    # Player turn: hit or stand
    while True:
        total = calculate_hand(player_hand)
        if total >= 21:
            break
        action = input("Hit or Stand? (h/s): ").lower()
        if action == 'h':
            new_card = shoe.deal_next_card()
            player_hand.append(new_card)
            print(f"You drew {new_card} -> hand total {calculate_hand(player_hand)}")
        else:
            break

    # Dealer turn: hit until 17+
    while calculate_hand(dealer_hand) < 17:
        dealer_hand.append(shoe.deal_next_card())

    player_total = calculate_hand(player_hand)
    dealer_total = calculate_hand(dealer_hand)

    print(f"Your final hand: {display_hand(player_hand)} -> total {player_total}")
    print(f"Dealer final hand: {display_hand(dealer_hand)} -> total {dealer_total}")

    # Determine outcome
    if player_total > 21:
        print("Bust! You lose your bet.")
    elif dealer_total > 21 or player_total > dealer_total:
        print("You win!")
        adjust_balance(bet * 2)  # win doubles bet
    elif player_total == dealer_total:
        print("Push! Bet returned.")
        adjust_balance(bet)
    else:
        print("Dealer wins! You lose your bet.")

    print(f"Balance after round: ${show_balance()}")
    print("-" * 30)

def main():
    print("Welcome to Blackjack!")
    while show_balance() > 0:
        play_round()
        cont = input("Do you want to play another round? (y/n): ").lower()
        if cont != 'y':
            break
    print(f"Game over! Final balance: ${show_balance()}")

if __name__ == "__main__":
    main()
