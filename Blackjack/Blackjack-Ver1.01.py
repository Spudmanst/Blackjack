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

# Create deck of cards then shuffle
suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

cards = []

for suit in suits:
    for value in values:
        cards.append(f"{value} of {suit}")
        
random.shuffle(cards)

# Set scores for cards and players start at 0
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

def stdSleep():
    time.sleep(0.95)

def susSleep():
    time.sleep(1.5)
    
# Provide both dealer and player with 2 cards
playerHand = [cards.pop() for x in range(2)]
dealerHand = [cards.pop() for x in range(2)]


slowType(f"Your hand: {playerHand[0]} and {playerHand[1]}")
stdSleep()
slowType(f"Dealer's hand: {dealerHand[0]} and unknown")
stdSleep()

# Calculate scores for player and dealer
playerScore = sum(scores[card.split()[0]] for card in playerHand)
dealerScore = sum(scores[card.split()[0]] for card in dealerHand)

# Check for Blackjacks and resolve accordingly
if dealerScore == 21 and playerScore != 21:
    slowType(f"Dealer reveals hand: {dealerHand[0]} and {dealerHand[1]}\nDealer has Blackjack and you don't. You lose.")
    exit()
elif dealerScore != 21 and playerScore == 21:
    slowTypeNoLine(f"BLACKJACK!\nDealer reveals hand: {dealerHand[0]} and ")
    susSleep()
    slowType(f"{dealerHand[1]}\nDealer cannot match. You win!")
    exit()
elif dealerScore == 21 and playerScore == 21:
    slowTypeNoLine(f"BLACKJACK!\nDealer reveals hand: {dealerHand[0]} and ")
    susSleep()
    slowType(f"{dealerHand[1]}\nBoth you and the the Dealer have Blackjack. It's a tie!")
    exit()
else:
    slowType(f"Your Score: {playerScore}")

stdSleep()

# Ask player for input while not "bust"
while playerScore < 21:
    action = input("What would you like to do, '(H)it' or '(S)tick'?\n").lower()

    if action == "hit" or action == "h":
        newCard = cards.pop()
        playerHand.append(newCard)
        playerScore += scores[newCard.split()[0]]
        if playerScore > 21:
            playerScore = adjustForAces(playerHand)
        slowType(f"Card received: {newCard}\nNew score: {playerScore}")
        stdSleep()
    elif action == "stick" or action == "s":
        stdSleep()
        break
    elif action == "exit" or action == "e":
        exit()
    else:
        print(f"Unknown command, type 'hit' or 'stick' to continue.\nType 'exit' to finish playing")

if playerScore > 21:
    slowType("Bust! You lose.")
    exit()
    
# Dealer to play
slowType(f"Dealer reveals hand: {dealerHand[0]} and {dealerHand[1]}\nDealer's score = {dealerScore}")
stdSleep()

while dealerScore < 17:
    newCard = cards.pop()
    dealerHand.append(newCard)
    dealerScore += scores[newCard.split()[0]]
    dealerScore = adjustForAces(dealerHand)
    slowType(f"Dealer receives: {newCard}\nDealer's new score: {dealerScore}")
    stdSleep()

if dealerScore > 21:
    slowType(f"Dealer Bust. You win!")
elif dealerScore > playerScore:
    slowType(f"Dealer Wins with {dealerScore} vs your {playerScore}.")
elif dealerScore < playerScore:
    slowType(f"You win with {playerScore} vs Dealer's {dealerScore}!")
else:
    slowType("It's a tie!")
