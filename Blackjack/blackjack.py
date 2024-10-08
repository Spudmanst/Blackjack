import random
import time

# Test

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
def adjustForAces(score, hand):
    aceCount = sum(1 for card in hand if card.split()[0] == "Ace")
    while score > 21 and aceCount > 0:
        score -= 10
        aceCount -= 1
    return score

# Provide both dealer and player with 2 cards
playerHand = [cards.pop() for x in range(2)]
dealerHand = [cards.pop() for x in range(2)]


print(f"Your hand: {playerHand[0]} and {playerHand[1]}")
time.sleep(0.5)
print(f"Dealer's hand: {dealerHand[0]} and unknown")
time.sleep(1)

# Calculate scores for player
playerScore = scores[playerHand[0].split()[0]] + scores[playerHand[1].split()[0]]

print(f"Your Score: {playerScore}")
time.sleep(1)

# Ask player for input while not "bust"
while playerScore < 21:
    action = input("What would you like to do, '(H)it' or '(S)tick'?\n").lower()

    if action == "hit" or action == "h":
        newCard = cards.pop()
        playerHand.append(newCard)
        playerScore += scores[newCard.split()[0]]
        if playerScore > 21:
            playerScore = adjustForAces(playerScore, playerHand)
        print(f"Card received: {newCard}\nNew score: {playerScore}")
        time.sleep(1)
    elif action == "stick" or action == "s":
        time.sleep(1)
        break
    elif action == "exit" or action == "e":
        exit()
    else:
        print(f"Unknown command, type 'hit' or 'stick' to continue.\nType 'exit' to finish playing")

if playerScore > 21:
    print("Bust! You lose.")
    exit()
    
# Dealer to play
dealerScore = scores[dealerHand[0].split()[0]] + scores[dealerHand[1].split()[0]]
print(f"Dealer reveals hand: {dealerHand[0]} and {dealerHand[1]}\nDealer's score = {dealerScore}")
time.sleep(1)

while dealerScore < 17:
    newCard = cards.pop()
    dealerHand.append(newCard)
    dealerScore += scores[newCard.split()[0]]
    dealerScore = adjustForAces(dealerScore, dealerHand)
    print(f"Dealer receives: {newCard}\nDealer's new score: {dealerScore}")
    time.sleep(1)

if dealerScore > 21:
    print(f"Dealer Bust. You win!")
elif dealerScore > playerScore:
    print(f"Dealer Wins with {dealerScore} vs your {playerScore}.")
elif dealerScore < playerScore:
    print(f"You win with {playerScore} vs Dealer's {dealerScore}!")
else:
    print("It's a tie!")
