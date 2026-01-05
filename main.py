# main.py

from games.blackjack import main as blackjack_main
from core.player import balance


def main():
    print("Welcome to the Casino!")
    print("You are the player, using your balance from player.py. You currently have a balance of $", balance )
    print("Starting a game of Blackjack...\n")

    blackjack_main()  # Start the blackjack game loop


if __name__ == "__main__":
    main()


