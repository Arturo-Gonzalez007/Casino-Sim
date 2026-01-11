# main.py
from ui.menu import main as start_window
from games.blackjack import play_round
from core.player import balance


def main():
    start_window()

if __name__ == "__main__":
    main()
