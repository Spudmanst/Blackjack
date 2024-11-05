from . import options
from . import playing_cards
from . import text_effect
from . import winnings
import sys

# Constants for game limits
MIN_PLAYERS = 1
MAX_PLAYERS = 7
MIN_CASH = 10
MAX_CASH = 10000
MIN_ROUNDS = 1
MAX_ROUNDS = 10

class Player:
    def __init__(self, name, number, active = True, bet = 0, cash = 0, hand = [], hand_size = 0, in_game = True, score = 0, win = None):
        self.name = name
        self.number = number
        self.active = active
        self.bet = bet
        self.cash = cash
        self.hand = hand
        self.hand_size = hand_size
        self.in_game = in_game
        self.score = score
        self.win = win

def new_round(player):
    player.win = None
    player.bet = 0
    player.hand = []
    
num_of_packs = int(options.variations["num_of_packs"])

def start_game(): 
    # Get number of players
    while True:
        try:
            num_of_players = int(text_effect.slow_input(f"How many players would you like? Minimum {MIN_PLAYERS}, Maximum {MAX_PLAYERS}: "))
            if MIN_PLAYERS <= num_of_players <= MAX_PLAYERS:
                break
            else:
                print(f"Invalid input, must use a number between {MIN_PLAYERS} - {MAX_PLAYERS} to continue.")
        except ValueError:
            print(f"Invalid input, please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
    
    while True:
        try:       
            named_players = text_effect.slow_input("Are players going to give names, Yes or No?: ").lower()
                
            if named_players not in ("yes", "y", "no", "n"):
                    print("Invalid input, please enter 'yes' or 'no'")
                    continue
            else:
                break
        except Exception as e:
            print("An error occurred: ", e)
                        
    while True:
        try:
            starting_cash = int(text_effect.slow_input(f"How many money should all players start with? Minimum ${MIN_CASH}, Maximum ${MAX_CASH}: $"))
            if MIN_CASH <= starting_cash <= MAX_CASH:
                break
            else:
                print(f"Invalid input, must use a whole number between {MIN_CASH} and {MAX_CASH} to continue.")
        except ValueError:
            print(f"Invalid input, please enter a whole number between {MIN_CASH} and {MAX_CASH} (don't use commas).")
            
    while True:
        try:
            num_of_rounds = int(text_effect.slow_input(f"How many rounds would you like? Minimum {MIN_ROUNDS}, Maximum {MAX_ROUNDS}: "))
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
                name = text_effect.slow_input(f"Enter the name for Player {player_num}: ") 
                # Check for duplicate name
                if any(name == player.name for player in players):
                    text_effect.slow_type("Name already in use, please enter another name.")
                else:
                    break # Exit loop if name not duplicate
            else:
                name = str(player_num)
                break # Need to break loop if we are not using names as using while True to loop until all names are unique.
            
        player = Player(number = player_num, name = name, cash = starting_cash)
        
        players.append(player)
          
    round_number = 1
    cards = ()
    
    while round_number <= num_of_rounds:
        text_effect.divide_lines()
        print(f"ROUND {round_number}")
        text_effect.divide_lines()
        if len(cards) <= 26 * num_of_packs or len(cards) <= 40: # 26 is a half of 52
            cards = playing_cards.create_shuffled_deck(num_of_packs)
            text_effect.slow_type("***Deck has been shuffled***")
            text_effect.divide_lines()
        # Uncomment the below if you need to check if the creation of the deck is working correctly.    
        """
        for card in cards:
            print(f"{card}", end=" | ")
        print("\n")
        """
        text_effect.std_sleep()
        
        for player in players:
            # Exclude asking players how much to bet if we already know they do not have the money.
            if player.in_game:
                while True:
                    try:
                        bet = text_effect.slow_input(f"How much is Player {player.name} betting (cash remaining: {text_effect.format_cash(player.cash)})? $")
                        bet = int(bet)
                        
                        if bet > player.cash:
                            print(f"Not enough funds, maximum available to Player {player.name} is {text_effect.format_cash(player.cash)}.")
                        elif bet < 1:
                            print("Must bet at least $1 or more")
                        else:
                            player.bet = bet
                            break
                    except ValueError:
                        print(f"Invalid input, please enter a whole number between $1.00 and {text_effect.format_cash(player.cash)}.")
                        
        text_effect.sleep_line()
        
        # Deal cards to all active players and calculate scores
        for player in players:
            if player.active:
                player.hand = [cards.pop() for _ in range(2)]
                player.score = winnings.calculate_score(player.hand)
                # Comment out above line if you wish to test when players having specific score
                # player.score = 21
                if player.score == 21:
                    player.win = "Blackjack"
        
        # Deal cards to dealer and check for Blackjack            
        dealer_hand = [cards.pop() for _ in range(2)]
        dealer_score = winnings.calculate_score(dealer_hand)
        # Comment out above line if you wish to test when dealer having specific score
        # dealer_score = 21
        winnings.dealer_has_blackjack(dealer_score)
        
        # Check if all active players have Blackjack
        all_players_blackjack = all(player.win == "Blackjack" for player in players if player.active)
        
        # If Dealer has Blackjack then skip normal game process as they can only match Blackjack to draw/push/tie.
        if winnings.dealer_blackjack == True:
            text_effect.slow_type(f"Dealer reveals hand: {dealer_hand[0]} and {dealer_hand[1]}\nDealer has Blackjack.")
            
            for player in players:
                if player.active:
                    text_effect.slow_type(f"Player {player.name}'s hand: {player.hand[0]} and {player.hand[1]}")
                    if player.win == "Blackjack":
                        text_effect.slow_type(f"Player {player.name} has Blackjack!")
                        player.win = "Push"
                    else:
                        player.win = "Dealer_blackjack"
                text_effect.divide_lines()
            
            if all_players_blackjack:
                text_effect.slow_type("All participating players have Blackjack!")
                text_effect.divide_lines()
                        
            text_effect.std_sleep()      
        
        # If all active players have Blackjack, then skip normal game process. We know dealer doesn't have Blackjack from "if" statement.
        elif all_players_blackjack and not winnings.dealer_blackjack:
            for player in players:
                if player.active:
                    text_effect.slow_type(f"Player {player.name}'s hand: {player.hand[0]} and {player.hand[1]}")
                    player.win = "Blackjack"
            text_effect.slow_type("All participating players have Blackjack. What about the dealer?")
            text_effect.sus_sleep()
            text_effect.slow_type(f"Dealer reveals hand: {dealer_hand[0]} and {dealer_hand[1]}\nDealer could not match, all players win!")
            text_effect.sleep_line()
       
        # If no one has Blackjack then normal game play.    
        else:
            # Players have their turn
            for player in players:
                if player.active:
                    text_effect.slow_type(f"Dealer's hand: {dealer_hand[0]} and unknown")
                    text_effect.slow_type(f"Player {player.name}'s hand: {player.hand[0]} and {player.hand[1]}")
                    
                    # Auto "stand" players on 21, otherwise ask what they would like to do.
                    if player.score == 21:
                        text_effect.slow_type("Blackjack!")
                        player.win = "Blackjack"
                        text_effect.divide_lines()
                        continue # End current player's turn
                    else: 
                        text_effect.slow_type(f"Player {player.name}'s score: {player.score}")
                        
                    while player.score < 21:
                        action = text_effect.slow_input("What would you like to do, '(H)it' or '(S)tand'? ").lower()

                        if action in ("hit", "h"):
                            new_card = cards.pop()
                            player.hand.append(new_card)
                            player.score = winnings.calculate_score(player.hand)
                            text_effect.slow_type(f"Card received: {new_card}\nNew score: {player.score}")
                            # If player has 5 Card Charlie then end turn
                            if winnings.charlie_check(player.hand, player.score) == "Charlie":
                                player.win = "Charlie"
                                text_effect.slow_type(f"Player {player.name} has 5-Card Charlie!")
                                break
                        elif action in ("stand", "s"):
                            text_effect.slow_type(f"Player {player.name} is stands with a score of {player.score}")
                            break
                        elif action in ("exit", "e"):
                            print("Exiting game.")
                            exit()
                        else:
                            print(f"Unknown command, type 'hit' or 'stand' to continue.\nType 'exit' to finish playing")

                    if player.score > 21:
                        text_effect.slow_type(f"Player {player.name} busts!")
                        player.active = False
                        player.win = "Bust"
                    
                    text_effect.sleep_line()

            # Dealer plays if not all players are out and not all players have Blackjack
            all_players_out = all(not player.active for player in players)

            if all_players_out:
                text_effect.slow_type("All players are out.")
            elif all_players_blackjack and winnings.dealer_blackjack == False:
                continue
            else:
                text_effect.slow_type(f"Dealer reveals hand: {dealer_hand[0]} and {dealer_hand[1]}")
                text_effect.slow_type(f"Dealer's score = {dealer_score}")

                text_effect.std_sleep()

                # Dealer must obtain new card until their score is above 16 (casino rules)
                while dealer_score < 17:
                    new_card = cards.pop()
                    dealer_hand.append(new_card)
                    dealer_score = winnings.calculate_score(dealer_hand)
                    text_effect.slow_type(f"Dealer receives: {new_card}\nDealer's new score: {dealer_score}")
                
                if dealer_score > 21:
                    text_effect.slow_type("Dealer has busted!")
                
            text_effect.sleep_line() # Create divider when dealer has finished

        # Calculate winners and winnings
        for player in players:
            if player.in_game:
                winnings.winner(dealer_score, player)
                player.cash += winnings.player_payout(player.win, player.bet)
            
        text_effect.sleep_line() 
        
        if round_number < num_of_rounds:
            for player in players:
                if player.in_game:
                    if player.cash < 1:
                        text_effect.slow_type(f"Player {player.name} doesn't have enough funds to bet! They are removed from the game!")
                        player.in_game = False
                        new_round(player) # wipe to ensure no issues going forward.
                    else:
                        text_effect.slow_type(f"Player {player.name} has {text_effect.format_cash(player.cash)} remaining.")
                        player.active = True # Change back to true in case they busted this round but still have money for next round
                        new_round(player)
        
        text_effect.sus_sleep()
        
        # Check if anyone can bet, if not then end game
        no_one_can_bet = all(player.in_game == False for player in players)
        if no_one_can_bet:
            text_effect.divide_lines()
            text_effect.slow_type("No players have any cash to bet with! Ending game.")
            text_effect.divide_lines()
            break
        else:        
            round_number += 1
    
    # When the game is over, print out scores and advise on winner
    if round_number > num_of_rounds:
        # Sort the players by cash in descending order
        sorted_players = sorted(players, key=lambda player: player.cash, reverse=True)

        # Print out the sorted list
        text_effect.slow_type("FINAL SCOREBOARD")
        text_effect.divide_lines()
        for player in sorted_players:
            text_effect.slow_type(f"Player {player.name}: ${player.cash:.2f}")
        text_effect.divide_lines()