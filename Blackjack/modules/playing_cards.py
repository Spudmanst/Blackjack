import random

def create_shuffled_deck(num_decks = 1):
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    single_deck = [f"{value} of {suit}" for suit in suits for value in values]
    deck = single_deck * num_decks
    random.shuffle(deck)
    return deck

scores = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11
}