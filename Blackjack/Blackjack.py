# Blackjack version 1.01

import random
import time
import sys

def slowType(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Flush the output to ensure it prints immediately
        time.sleep(delay)   # Delay between each character
    # Ensure a new line at the end
    sys.stdout.write('\n')
    sys.stdout.flush()
    
def slowTypeNoLine(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Flush the output to ensure it prints immediately
        time.sleep(delay)   # Delay between each character

suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
cards = [f"{value} of {suit}" for suit in suits for value in values]
random.shuffle(cards)

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
def adjustForAces(hand):
    score = sum(scores[card.split()[0]] for card in hand)
    aceCount = sum(1 for card in hand if card.split()[0] == "Ace")
    while score > 21 and aceCount > 0:
        score -= 10
        aceCount -= 1
    return score

# Minor delay functions for gameplay
def stdSleep():
    time.sleep(0.95)

def susSleep():
    time.sleep(1.5)

# Get number of players
while True:
    try:
         numOfPlayers = int(input("How many players would you like? Minimum 1, Maximum 7: "))
         if 1 <= numOfPlayers <= 7:
             break
         else:
             slowType("Invalid input, must use a number between 1 - 7 to continue.")
    except ValueError:
        slowType("Invalid input, please enter a number between 1 and 7.")

# Deal cards to players
player_hands = {player: [cards.pop() for _ in range(2)] for player in range(1, numOfPlayers + 1)}
dealerHand = [cards.pop() for _ in range(2)]

# Calculate scores for players
player_score = {player: sum(scores[card.split()[0]] for card in player_hands[player]) for player in range(1, numOfPlayers + 1)}
dealerScore = sum(scores[card.split()[0]] for card in dealerHand)

# Initialize player win status
player_win = {player: None for player in range(1, numOfPlayers + 1)}

# Players have their turn
for player in range(1, numOfPlayers + 1):
    slowType(f"Dealer's hand: {dealerHand[0]} and unknown")
    slowType(f"Player {player}'s hand: {player_hands[player][0]} and {player_hands[player][1]}")
    
    if player_score[player] == 21:
        slowType("Blackjack!")
        player_score[player] = "Blackjack"
        continue # End current player's turn
    else: 
        slowType(f"Player {player}'s score: {player_score[player]}")
        
    while player_score[player] < 21:
        action = input("What would you like to do, '(H)it' or '(S)tick'?\n").lower()

        if action in ("hit", "h"):
            newCard = cards.pop()
            player_hands[player].append(newCard)
            player_score[player] += scores[newCard.split()[0]]
            if player_score[player] > 21:
                player_score[player] = adjustForAces(player_hands[player])
            slowType(f"Card received: {newCard}\nNew score: {player_score[player]}")
            stdSleep()
        elif action in ("stick", "s"):
            stdSleep()
            break
        elif action in ("exit", "e"):
            exit()
        else:
            print(f"Unknown command, type 'hit' or 'stick' to continue.\nType 'exit' to finish playing")

    if player_score[player] > 21:
        slowType(f"Player {player} busts!")
        player_win[player] = "Bust"
    
    stdSleep()

# Dealer plays
slowType(f"Dealer reveals hand: {dealerHand[0]} and {dealerHand[1]}")

if dealerScore == 21:
    slowType("Dealer has Blackjack.")
else:
    slowType(f"Dealer's score = {dealerScore}")

stdSleep()

while dealerScore < 17:
    newCard = cards.pop()
    dealerHand.append(newCard)
    dealerScore += scores[newCard.split()[0]]
    dealerScore = adjustForAces(dealerHand)
    slowType(f"Dealer receives: {newCard}\nDealer's new score: {dealerScore}")
    stdSleep()

# Calculate winners
for player in range(1, numOfPlayers +1):
    if player_win[player] is None:
        if player_score[player] > dealerScore and player_score[player] <= 21:
            player_win[player] = True
            slowType(f"Player {player} wins with {player_score[player]} vs the Dealer's {dealerScore}!")
        elif player_score[player] == dealerScore:
            player_win[player] = "Tie"
            slowType(f"Player {player} ties with {player_score[player]}!")
        else:
            player_win[player] = False
            slowType(f"Player {player} loses with {player_score[player]} vs the Dealer's {dealerScore}!")
    elif player_win[player] == "Blackjack":
        slowType(f"Player {player} wins with Blackjack!")
    else:
        slowType(f"Player {player} busted!")