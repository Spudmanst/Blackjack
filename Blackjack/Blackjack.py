# Blackjack version 1.04

import random
import time
import sys

def slow_type(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Flush the output to ensure it prints immediately
        time.sleep(delay)   # Delay between each character
    # Ensure a new line at the end
    sys.stdout.write('\n')
    sys.stdout.flush()
    
def slow_type_no_line(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Flush the output to ensure it prints immediately
        time.sleep(delay)   # Delay between each character

def create_shuffled_deck():
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    deck = [f"{value} of {suit}" for suit in suits for value in values]
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

# Prep to check for Aces If player "bust" and change score
def adjust_for_aces(hand):
    score = sum(scores[card.split()[0]] for card in hand)
    ace_count = sum(1 for card in hand if card.split()[0] == "Ace")
    while score > 21 and ace_count > 0:
        score -= 10
        ace_count -= 1
    return score

# Minor delay functions for gameplay
def std_sleep():
    time.sleep(0.95)

def sus_sleep():
    time.sleep(1.5)
    
def divide_lines():
    print("----------")

def start_game():
    cards = create_shuffled_deck()
    
    # Get number of players
    while True:
        try:
            num_of_players = int(input("How many players would you like? Minimum 1, Maximum 7: "))
            if 1 <= num_of_players <= 7:
                break
            else:
                slow_type("Invalid input, must use a number between 1 - 7 to continue.")
        except ValueError:
            slow_type("Invalid input, please enter a number between 1 and 7.")

    # Deal cards to players
    player_hands = {player: [cards.pop() for _ in range(2)] for player in range(1, num_of_players + 1)}
    dealer_hand = [cards.pop() for _ in range(2)]

    # Calculate scores for players
    player_score = {player: adjust_for_aces(player_hands[player]) for player in range(1, num_of_players + 1)}
    dealer_score = adjust_for_aces(dealer_hand)

    # Initialize player win status
    player_win = {player: None for player in range(1, num_of_players + 1)}

    # Players have their turn
    for player in range(1, num_of_players + 1):
        slow_type(f"Dealer's hand: {dealer_hand[0]} and unknown")
        slow_type(f"Player {player}'s hand: {player_hands[player][0]} and {player_hands[player][1]}")
        
        if player_score[player] == 21:
            slow_type("Blackjack!")
            player_win[player] = "Blackjack"
            divide_lines()
            continue # End current player's turn
        else: 
            slow_type(f"Player {player}'s score: {player_score[player]}")
            
        while player_score[player] < 21:
            action = input("What would you like to do, '(H)it' or '(S)tick'?\n").lower()

            if action in ("hit", "h"):
                new_card = cards.pop()
                player_hands[player].append(new_card)
                player_score[player] += scores[new_card.split()[0]]
                if player_score[player] > 21:
                    player_score[player] = adjust_for_aces(player_hands[player])
                slow_type(f"Card received: {new_card}\nNew score: {player_score[player]}")
            elif action in ("stick", "s"):
                slow_type(f"Player {player} is sticking with a score of {player_score[player]}")
                break
            elif action in ("exit", "e"):
                print("Exiting game.")
                exit()
            else:
                print(f"Unknown command, type 'hit' or 'stick' to continue.\nType 'exit' to finish playing")

        if player_score[player] > 21:
            slow_type(f"Player {player} busts!")
            player_win[player] = "Bust"
        
        elif player_score[player] == 21 and player_win[player] != "Blackjack":
            slow_type(f"Player {player} is sticking with a score of {player_score[player]}")
        
        divide_lines()
        std_sleep()

    # Dealer plays
    slow_type(f"Dealer reveals hand: {dealer_hand[0]} and {dealer_hand[1]}")

    if dealer_score == 21:
        slow_type("Dealer has Blackjack.")
    else:
        slow_type(f"Dealer's score = {dealer_score}")

    std_sleep()

    while dealer_score < 17:
        new_card = cards.pop()
        dealer_hand.append(new_card)
        dealer_score += scores[new_card.split()[0]]
        dealer_score = adjust_for_aces(dealer_hand)
        slow_type(f"Dealer receives: {new_card}\nDealer's new score: {dealer_score}")
    
    if dealer_score > 21:
        slow_type("Dealer has busted!")
        
    divide_lines() # Create divider when dealer has finished
    std_sleep()

    # Calculate winners
    for player in range(1, num_of_players +1):
        if player_win[player] is None:
            if dealer_score > 21:
                player_win[player] = True
                slow_type(f"Player {player} wins as the Dealer busted!")
            elif player_score[player] > dealer_score and player_score[player] <= 21:
                player_win[player] = True
                slow_type(f"Player {player} wins with {player_score[player]} vs the Dealer's {dealer_score}!")
            elif player_score[player] == dealer_score:
                player_win[player] = "Tie"
                slow_type(f"Player {player} ties with {player_score[player]}!")
            else:
                player_win[player] = False
                slow_type(f"Player {player} loses with {player_score[player]} vs the Dealer's {dealer_score}!")
        elif player_win[player] == "Blackjack":
            slow_type(f"Player {player} wins with Blackjack!")
        else:
            slow_type(f"Player {player} busted!")
            

while True:
    start_game()

    action = input("What would you like to do? (R)eplay, (E)xit: ").lower()

    if action in ("replay", "r"):
        divide_lines()
        start_game()
    elif action in ("exit", "e"):
        print("Exiting game.")
        divide_lines()
        break
    else:
        slow_type("Unknown command, type 'replay' or 'exit'.")