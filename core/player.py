# player.py
balance = 1000  # your starting balance


def adjust_balance(amount):
    global balance
    balance += amount


def show_balance():
    return balance
