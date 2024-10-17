# Blackjack version 1.2.0

import random
import time
import sys

# Prep to check for Aces If player "bust" and change score
def adjust_for_aces(hand):
    score = sum(scores[card.split()[0]] for card in hand)
    ace_count = sum(1 for card in hand if card.split()[0] == "Ace")
    while score > 21 and ace_count > 0:
        score -= 10
        ace_count -= 1
    return score

def charlie_check(hand, score):
    if len(hand) == 5 and score < 22:
        return "Charlie"
    else:
        return "None"

def create_shuffled_deck():
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    deck = [f"{value} of {suit}" for suit in suits for value in values]
    random.shuffle(deck)
    return deck
    
def divide_lines():
    print("----------")

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

# Minor delay functions for gameplay
def std_sleep():
    time.sleep(0.95)

def sus_sleep():
    time.sleep(1.5)

def start_game(): 
    # Get number of players
    while True:
        try:
            num_of_players = int(input("How many players would you like? Minimum 1, Maximum 7: "))
            if 1 <= num_of_players <= 7:
                break
            else:
                print("Invalid input, must use a number between 1 - 7 to continue.")
        except ValueError:
            print("Invalid input, please enter a number between 1 and 7.")
            
    while True:
        try:
            num_of_rounds = int(input("How many rounds would you like? Minimum 1, Maximum 10: "))
            if 1 <= num_of_rounds <= 10:
                break
            else:
                print("Invalid input, must use a number between 1 - 10 to continue.")
        except ValueError:
            print("Invalid input, please enter a number between 1 and 10.")
    
    round_number = 1
    
    while round_number <= num_of_rounds:
        divide_lines()
        print(f"ROUND {round_number}")
        divide_lines() 
        cards = create_shuffled_deck()
        sus_sleep()

        # Deal cards to players
        player_hands = {player: [cards.pop() for _ in range(2)] for player in range(1, num_of_players + 1)}
        dealer_hand = [cards.pop() for _ in range(2)]

        # Calculate scores for players
        player_score = {player: adjust_for_aces(player_hands[player]) for player in range(1, num_of_players + 1)}
        dealer_score = adjust_for_aces(dealer_hand)

        # Initialize player win status
        player_win = {player: None for player in range(1, num_of_players + 1)}
        
        if dealer_score == 21:
            slow_type(f"Dealer reveals hand: {dealer_hand[0]} and {dealer_hand[1]}\nDealer has Blackjack.")
            
            any_player_has_blackjack = False
            
            for player in range(1, num_of_players + 1):
                slow_type(f"Player {player}'s hand: {player_hands[player][0]} and {player_hands[player][1]}")
                
                if player_score[player] == 21:
                    slow_type("Blackjack!")
                    player_win[player] = "Push"
                    any_player_has_blackjack = True
                else:
                    player_win[player] = "False"
                    
                std_sleep()
            
            if not any_player_has_blackjack:
                slow_type("All players lose as none can match the Dealer's Blackjack.")
            else:        
                for player in range(1, num_of_players +1):
                    if player_win[player] is "Push":
                        slow_type(f"Player {player} matches Blackjack. Push!")
                    else:
                        slow_type(f"Player {player} loses as they could not match the Dealer's Blackjack.")

        else:
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
                    action = input("What would you like to do, '(H)it' or '(S)tick'? ").lower()

                    if action in ("hit", "h"):
                        new_card = cards.pop()
                        player_hands[player].append(new_card)
                        player_score[player] += scores[new_card.split()[0]]
                        if player_score[player] > 21:
                            player_score[player] = adjust_for_aces(player_hands[player])
                        slow_type(f"Card received: {new_card}\nNew score: {player_score[player]}")
                        if charlie_check(player_hands[player], player_score[player]) == "Charlie":
                            player_win[player] = "Charlie"
                            slow_type(f"Player {player} has 5-Card Charlie!")
                            break
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
                elif player_win[player] == "Charlie":
                    slow_type(f"Player {player} wins with 5-Card Charlie!")
                else:
                    slow_type(f"Player {player} busted!")
        
        sus_sleep()        
        round_number += 1
            
print(f"""
  ____  _            _        _            _    _
 |  _ \| |          | |      | |          | |  | |
 | |_) | | __ _  ___| | __   | | __ _  ___| | _| |
 |  _ <| |/ _` |/ __| |/ /   | |/ _` |/ __| |/ / |
 | |_) | | (_| | (__|   < |__| | (_| | (__|   <|_|
 |____/|_|\__,_|\___|_|\_\____/ \__,_|\___|_|\_(_)
                                                  """)

while True:
    start_game()

    while True:
        action = input("What would you like to do? (R)eplay, (E)xit: ").lower()

        if action in ("replay", "r"):
            divide_lines()
            break
        elif action in ("exit", "e"):
            print("Exiting game.")
            divide_lines()
            sys.exit()
        else:
            print("Unknown command, type 'replay' or 'exit'.")