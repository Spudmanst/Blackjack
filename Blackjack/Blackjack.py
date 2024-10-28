# Blackjack version 2.4.0

import random
import time
import sys

# Constants for game limits
MIN_PLAYERS = 1
MAX_PLAYERS = 7
MIN_CASH = 10
MAX_CASH = 10000
MIN_ROUNDS = 1
MAX_ROUNDS = 10

class Player:
    def __init__(self, name, number, bet = 0, cash = 0, hand = [], hand_size = 0, score = 0, win = None):
        self.name = name
        self.number = number
        self.bet = bet
        self.cash = cash
        self.hand = hand
        self.hand_size = hand_size
        self.score = score
        self.win = win

# Prep to check for Aces If player "bust" and change score
def calculate_score(hand):
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

# Help with splitting screen to make things easier to read where required
def divide_lines():
    print("----------")
    
# Gobal variable used if dealer has Blackjack to skip large parts of coding. 
def dealer_has_blackjack(score):
    global dealer_blackjack
    if score == 21:
        dealer_blackjack = True
    else:
        dealer_blackjack = False
    
# Helper Function for printing player money to specific format
def format_cash(player_cash_value):
    return f"${player_cash_value:.2f}"

def player_payout(win, bet):
    if win == "Blackjack":
        return (bet * 1.5)
    elif win == "Charlie":
        return (bet * 1.2)
    elif win == False:
        return (-bet)
    elif win == "Push" or win == "did_not_bet":
        return 0 
    else: # Last left is True
        return bet

def player_payout_format(amount):
    return f"${abs(amount):.2f}"

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

# Both line and minor delay, indicating new phase
def sleep_line():
    divide_lines()
    std_sleep()

# Provide appearance of computer typing instead of text instantly appearing, slightly quicker 
def slow_input(prompt, delay=0.02):
    slow_type(prompt, delay, end='')  # No newline at the end
    return input()  # Capture user input on the same line

# Provide appearance of computer typing instead of text instantly appearing        
def slow_type(text, delay=0.02, end="\n"):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Flush the output to ensure it prints immediately
        time.sleep(delay)   # Delay between each character
    # Ensure a new line at the end
    if end:
        sys.stdout.write(end)
        sys.stdout.flush() # New line should automatically flush however we will include to ensure accurate behavior

# Minor delay function for gameplay
def std_sleep():
    time.sleep(0.95)

# Longer delay function to provide "suspense"
def sus_sleep():
    time.sleep(1.5)

def start_game(): 
    # Get number of players
    while True:
        try:
            num_of_players = int(slow_input(f"How many players would you like? Minimum {MIN_PLAYERS}, Maximum {MAX_PLAYERS}: "))
            if MIN_PLAYERS <= num_of_players <= MAX_PLAYERS:
                break
            else:
                print(f"Invalid input, must use a number between {MIN_PLAYERS} - {MAX_PLAYERS} to continue.")
        except ValueError:
            print(f"Invalid input, please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
    
    while True:
        try:       
            named_players = slow_input("Are players going to give names, Yes or No?: ").lower()
                
            if named_players not in ("yes", "y", "no", "n"):
                    print("Invalid input, please enter 'yes' or 'no'")
                    continue
            else:
                break
        except Exception as e:
            print("An error occurred: ", e)
                        
    while True:
        try:
            starting_cash = int(slow_input(f"How many money should all players start with? Minimum ${MIN_CASH}, Maximum ${MAX_CASH}: $"))
            if MIN_CASH <= starting_cash <= MAX_CASH:
                break
            else:
                print(f"Invalid input, must use a whole number between {MIN_CASH} and {MAX_CASH} to continue.")
        except ValueError:
            print(f"Invalid input, please enter a whole number between {MIN_CASH} and {MAX_CASH} (don't use commas).")
            
    while True:
        try:
            num_of_rounds = int(slow_input(f"How many rounds would you like? Minimum {MIN_ROUNDS}, Maximum {MAX_ROUNDS}: "))
            if MIN_ROUNDS <= num_of_rounds <= MAX_ROUNDS:
                break
            else:
                print(f"Invalid input, must use a number between {MIN_ROUNDS} - {MAX_ROUNDS} to continue.")
        except ValueError:
            print(f"Invalid input, please enter a number between {MIN_ROUNDS} and {MAX_ROUNDS}.")
    
    # Create empty list, ready to receive player information.
    players = []
    
    for player_num in range(1, num_of_players + 1):
        while True:
            if named_players in ("yes", "y"):
                name = slow_input(f"Enter the name for Player {player_num}: ") 
                # Check for duplicate name
                if any(name == player.name for player in players):
                    slow_type("Name already in use, please enter another name.")
                else:
                    break # Exit loop if name not duplicate
            else:
                name = str(player_num)
                break # Need to break loop if we are not using names as using while True to loop until all names are unique.
            
        player = Player(number = player_num, name = name, cash = starting_cash)
        
        players.append(player)
          
    round_number = 1
    
    while round_number <= num_of_rounds:
        # Check if anyone can bet, if not then end game
        no_one_can_bet = all(player.cash < 1 for player in players)
        if no_one_can_bet:
            slow_type("No players have any cash to bet with! Ending game.")
            divide_lines()
            break
        divide_lines()
        print(f"ROUND {round_number}")
        cards = create_shuffled_deck()
        sleep_line()
        
        for player in players:
            # Reset hand and win status to prevent errors from preceding rounds.
            player.bet = 0
            player.hand = []
            player.win = None
            # Assign people if they cannot bet for future use.
            if player.cash < 1:
                player.bet = 0
                player.win = "did_not_bet"
                slow_type(f"Player {player.name} doesn't have enough funds to bet!")
            else:
                while True:
                    try:
                        bet = slow_input(f"How much is Player {player.name} betting (cash remaining: {format_cash(player.cash)})? $")
                        bet = int(bet)
                        
                        if bet > player.cash:
                            print(f"Not enough funds, maximum available to Player {player.name} is {format_cash(player.cash)}.")
                        elif bet < 1:
                            print("Must bet at least $1 or more")
                        else:
                            player.bet = bet
                            break
                    except ValueError:
                        print(f"Invalid input, please enter a whole number between $1.00 and {format_cash(player.cash)}.")
                        
        sleep_line()
        
        # Deal cards to all players and calculate scores
        for player in players:
            if player.win != "did_not_bet":
                player.hand = [cards.pop() for _ in range(2)]
                player.score = calculate_score(player.hand)
                # Comment out above line if you wish to test when players having specific score
                # player.score = 21
                if player.score == 21:
                    player.win = "Blackjack"
        
        # Deal cards to dealer and check for Blackjack            
        dealer_hand = [cards.pop() for _ in range(2)]
        dealer_score = calculate_score(dealer_hand)
        # Comment out above line if you wish to test when dealer having specific score
        # dealer_score = 21
        dealer_has_blackjack(dealer_score)
        
        # Check if all active players have Blackjack
        all_players_blackjack = all(player.win == "Blackjack" for player in players if player.win != "did_not_bet")
        
        # If Dealer has Blackjack then skip normal game process as they can only match Blackjack to draw/push/tie.
        if dealer_blackjack == True:
            slow_type(f"Dealer reveals hand: {dealer_hand[0]} and {dealer_hand[1]}\nDealer has Blackjack.")
            
            for player in players:
                if player.win != "did_not_bet":
                    slow_type(f"Player {player.name}'s hand: {player.hand[0]} and {player.hand[1]}")
                    if player.win == "Blackjack":
                        slow_type(f"Player {player.name} has Blackjack!")
                        player.win = "Push"
                    else:
                        player.win = "Dealer_blackjack"
            
            if all_players_blackjack:
                slow_type("All participating players have Blackjack!")
                divide_lines()
                        
            std_sleep()      
        
        # If all active players have Blackjack, then skip normal game process. We know dealer doesn't have Blackjack from "if" statement.
        elif all_players_blackjack and not dealer_blackjack:
            for player in players:
                if player.win != "did_not_bet":
                    slow_type(f"Player {player.name}'s hand: {player.hand[0]} and {player.hand[1]}")
                    player.win = "Blackjack"
            slow_type("All participating players have Blackjack. What about the dealer?")
            sus_sleep()
            slow_type(f"Dealer reveals hand: {dealer_hand[0]} and {dealer_hand[1]}\nDealer could not match, all players win!")
            sleep_line()
       
        # If no one has Blackjack then normal game play.    
        else:
            # Players have their turn
            for player in players:
                if player.bet != 0:
                    slow_type(f"Dealer's hand: {dealer_hand[0]} and unknown")
                    slow_type(f"Player {player.name}'s hand: {player.hand[0]} and {player.hand[1]}")
                    
                    # Auto "stick" players on 21, otherwise ask what they would like to do.
                    if player.score == 21:
                        slow_type("Blackjack!")
                        player.win = "Blackjack"
                        divide_lines()
                        continue # End current player's turn
                    else: 
                        slow_type(f"Player {player.name}'s score: {player.score}")
                        
                    while player.score < 21:
                        action = slow_input("What would you like to do, '(H)it' or '(S)tick'? ").lower()

                        if action in ("hit", "h"):
                            new_card = cards.pop()
                            player.hand.append(new_card)
                            player.score = calculate_score(player.hand)
                            slow_type(f"Card received: {new_card}\nNew score: {player.score}")
                            # If player has 5 Card Charlie then end turn
                            if charlie_check(player.hand, player.score) == "Charlie":
                                player.win = "Charlie"
                                slow_type(f"Player {player.name} has 5-Card Charlie!")
                                break
                        elif action in ("stick", "s"):
                            slow_type(f"Player {player.name} is sticking with a score of {player.score}")
                            break
                        elif action in ("exit", "e"):
                            print("Exiting game.")
                            exit()
                        else:
                            print(f"Unknown command, type 'hit' or 'stick' to continue.\nType 'exit' to finish playing")

                    if player.score > 21:
                        slow_type(f"Player {player.name} busts!")
                        player.win = "Bust"
                    
                    sleep_line()

            # Dealer plays if not all players are out and not all players have Blackjack
            all_players_out = all(player.win == "Bust" or player.win == "did_not_bet" for player in players)

            if all_players_out:
                slow_type("All players are out.")
            elif all_players_blackjack and dealer_blackjack == False:
                continue
            else:
                slow_type(f"Dealer reveals hand: {dealer_hand[0]} and {dealer_hand[1]}")
                slow_type(f"Dealer's score = {dealer_score}")

                std_sleep()

                # Dealer must obtain new card until their score is above 16 (casino rules)
                while dealer_score < 17:
                    new_card = cards.pop()
                    dealer_hand.append(new_card)
                    dealer_score = calculate_score(dealer_hand)
                    slow_type(f"Dealer receives: {new_card}\nDealer's new score: {dealer_score}")
                
                if dealer_score > 21:
                    slow_type("Dealer has busted!")
                
            sleep_line() # Create divider when dealer has finished

        # Calculate winners and winnings
        for player in players:
            if player.win != "did_not_bet":
                if player.win == "Blackjack":
                    slow_type(f"Player {player.name} wins with Blackjack! Win {player_payout_format(player_payout(player.win, player.bet))}!")
                elif player.win == "Charlie":
                    slow_type(f"Player {player.name} wins with 5-Card Charlie! Win {player_payout_format(player_payout(player.win, player.bet))}!")
                elif player.win == "Dealer_blackjack":
                    player.win = False # Need to change to false now to ensure it deducts money
                    slow_type(f"Player {player.name} loses to dealer's Blackjack! Lose {player_payout_format(player_payout(player.win, player.bet))}!")
                elif player.win == "Push":
                    slow_type(f"Player {player.name} ties with Dealer's Blackjack! No Change!")
                elif player.win is None:
                    if dealer_score > 21:
                        player.win = True
                        slow_type(f"Player {player.name} wins as the Dealer busted! Win {player_payout_format(player_payout(player.win, player.bet))}!")
                    elif player.score > dealer_score and player.score <= 21:
                        player.win = True
                        slow_type(f"Player {player.name} wins with {player.score} vs the Dealer's {dealer_score}! Win {player_payout_format(player_payout(player.win, player.bet))}!")
                    elif player.score == dealer_score:
                        player.win = "Push"
                        slow_type(f"Player {player.name} ties with a score of {player.score}! No change!")
                    else:
                        player.win = False
                        slow_type(f"Player {player.name} loses with {player.score} vs the Dealer's {dealer_score}! Lose {player_payout_format(player_payout(player.win, player.bet))}!")
                else:
                    player.win = False
                    slow_type(f"Player {player.name} busted! Lose {player_payout_format(player_payout(player.win, player.bet))}!")
               
            player.cash += player_payout(player.win, player.bet)
            
        sleep_line() 
        
        if round_number < num_of_rounds:
            for player in players:
                slow_type(f"Player {player.name} has {format_cash(player.cash)} remaining.")
                # Need to reset player win status before restarting
                player.win = None
        
        sus_sleep()        
        round_number += 1
    
    # When the game is over, print out scores and advise on winner
    if round_number > num_of_rounds:
        # Sort the players by cash in descending order
        sorted_players = sorted(players, key=lambda player: player.cash, reverse=True)

        # Print out the sorted list
        slow_type("FINAL SCOREBOARD")
        divide_lines()
        for player in sorted_players:
            slow_type(f"Player {player.name}: ${player.cash:.2f}")
        divide_lines()
            
print(r"""
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
        action = slow_input("What would you like to do? (R)eplay, (E)xit: ").lower()

        if action in ("replay", "r"):
            divide_lines()
            break
        elif action in ("exit", "e"):
            print("Exiting game.")
            divide_lines()
            sys.exit()
        else:
            print("Unknown command, type 'replay' or 'exit'.")