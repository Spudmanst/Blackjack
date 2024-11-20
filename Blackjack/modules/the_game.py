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
    def __init__(self, name, number, active = True, bet = 0, cash = 0, 
                 dbl_avail = False, hand = [], hand_stand = False, hand_size = 0, 
                 in_game = True, insure = False, score = 0, split_avail = False,
                 win = None
        ):
        self.name = name
        self.number = number # number is used if they don't set names
        self.active = active # set false if player cannot act for rest of round
        self.bet = bet
        self.bet_dbl = bet # used if player "doubles"
        self.bet_split = bet # Not used yet, will do for future plans
        self.cash = cash
        self.dbl_avail = dbl_avail # set true if player can "double"
        self.hand1 = hand
        self.hand1_stand = hand_stand # set true when player "stands" on their main hand
        self.hand2 = hand
        self.hand2_stand = hand_stand # only used if player "splits" their hand
        self.in_game = in_game # set false if player cannot play rest of game
        self.insure = insure # set true if player does take insurance
        self.score = score
        self.score2 = score # only used if player "splits" their hand
        self.split_avail = split_avail # set true if player can "split"
        self.win1 = win
        self.win2 = win # only used if player "splits" their hand

# Reset key values at the start of the round.
def new_round(player):
    player.bet = 0
    player.bet_dbl = 0
    player.bet_split = 0
    player.dbl_avail = False
    player.hand1 = []
    player.hand1_stand = False
    player.hand2 = []
    player.hand2_stand = False
    player.insure = False
    player.score1 = 0
    player.score2 = 0
    player.split_avail = False
    player.win1 = None
    player.win2 = None
    
def player_actions(player, cards, charlie_on):
    # Set variables according to which hand is being used if player has split.
    if player.hand1_stand == False:
        hand = player.hand1
        score = player.score1
        win = player.win1
    else:
        hand = player.hand2
        score = player.score2
        win = player.win2
        text_effect.slow_type(f"---Player {player.name}'s second hand ---")
        text_effect.slow_type(f"Player {player.name}'s hand: {hand[0]} and {hand[1]}\nHand score: {score}")
    
    # If a player has blackjack then they will not be given the option to take an aciton,
    # therefore if this happens it can only be a Blackjack after a player splits    
    if score == 21:
        text_effect.slow_type("Blackjack!")
        win = "split_blackjack"
        
    else:
        while score < 21:
            action = text_effect.slow_input(f"What would you like to do, '(H)it'{", '(D)ouble' " if player.dbl_avail else ""}{", 'S(p)lit' " if player.split_avail else ""} or '(S)tand'? ").lower()

            if action in ("hit", "h") or (player.dbl_avail and action in ("double", "d")):
                # Remove the ability to split or double.
                if len(hand) == 2: # Remove future computations by only doing once
                    player.dbl_avail = False
                    player.split_avail = False
                    
                new_card = cards.pop()
                # Comment above line and uncomment below line if testing for 5 card charlie
                # new_card = "Ace of Tests"
                hand.append(new_card)
                score = winnings.calculate_score(hand)
                text_effect.slow_type(f"Card received: {new_card}\nNew score: {score}")
                
                # If player's "doubled" then take money from bet and end their turn.
                if action in ("double", "d"):
                    player.cash -= player.bet
                    player.bet_dbl += player.bet
                    break
                
                # If player has 5 Card Charlie then end turn
                if charlie_on == True:
                    if winnings.charlie_check(hand, score) == "Charlie":
                        win = "Charlie"
                        text_effect.slow_type(f"Player {player.name} has 5-Card Charlie!")
                        break
                    
            elif action in ("split", "p") and player.split_avail == True:
                # Remove the ability to split or double.
                player.dbl_avail = False
                player.split_avail = False
                
                # Split cards and create two hands for player, advise what is hand 1.
                split_card = hand.pop()
                new_card = cards.pop()
                hand.append(new_card)
                score = winnings.calculate_score(hand)
                text_effect.slow_type(f"Card received: {new_card}\nNew Hand: {hand[0]} and {hand[1]}\nNew score: {score}")
                player.hand2.append(split_card)
                player.hand2.append(cards.pop())
                player.score2 = winnings.calculate_score(player.hand2)
                
                # Remember to take cash for the split bet
                player.cash -= player.bet
                player.bet_split = player.bet
                
            elif action in ("stand", "s"):
                text_effect.slow_type(f"Player {player.name} stands with a score of {score}")
                break
            
            elif action in ("exit", "e"):
                print("Exiting game.")
                exit()
            else:
                print(f"Unknown command, please type an option to continue.\nAlternatively type 'exit' to finish playing")
            
    if score > 21:
        text_effect.slow_type(f"Player {player.name} busts!")
        win = "Bust"
        
    # set variables back into Player accordingly.
    if player.hand1_stand == False:
        player.hand1 = hand
        player.hand1_stand = True
        player.score1 = score
        player.win1 = win
    else:
        player.hand2 = hand
        player.score2 = score
        player.win2 = win
        
    if player.win1 == "Bust" and (player.win2 == "Bust" or len(player.hand2) == 0):
        player.active = False

def start_game(): 
    
    """
    Bring in required settings from options. Create variables to ensure we don't
    keep asking the computer to calculate these each time we wish to use them.
    Also grabbing the variables now when the game has started ensures we have the 
    most up to date settings incase the user changes them.
    """
    num_of_packs = int(options.variations["num_of_packs"])
    charlie_active = options.variations["5_card_charlie"]
    ins_active = options.variations["insurance"]
    s17_rule = options.variations["s17"]
    
    while True:
        try:
            num_of_players = int(text_effect.slow_input(
                f"How many players would you like? Minimum {MIN_PLAYERS}, Maximum {MAX_PLAYERS}: "
                ))
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
            starting_cash = int(text_effect.slow_input(
                f"How many money should all players start with? Minimum ${MIN_CASH}, Maximum ${MAX_CASH}: $"
                ))
            if MIN_CASH <= starting_cash <= MAX_CASH:
                break
            else:
                print(f"Invalid input, must use a whole number between {MIN_CASH} and {MAX_CASH} to continue.")
        except ValueError:
            print(f"Invalid input, please enter a whole number between {MIN_CASH} and {MAX_CASH} (don't use commas).")
            
    while True:
        try:
            num_of_rounds = int(text_effect.slow_input(
                f"How many rounds would you like? Minimum {MIN_ROUNDS}, Maximum {MAX_ROUNDS}: "
                ))
            if MIN_ROUNDS <= num_of_rounds <= MAX_ROUNDS:
                break
            else:
                print(f"Invalid input, must use a number between {MIN_ROUNDS} - {MAX_ROUNDS} to continue.")
        except ValueError:
            print(f"Invalid input, please enter a number between {MIN_ROUNDS} and {MAX_ROUNDS}.")
    
    # Create empty list, ready to receive player information.
    players = []
    
    for player_num in range(1, num_of_players + 1):
        while True: # While loop allows us to constantly ask for name if duplicate with another.
            if named_players in ("yes", "y"):
                name = text_effect.slow_input(f"Enter the name for Player {player_num}: ") 
                # Check for duplicate name
                if any(name == player.name for player in players):
                    text_effect.slow_type("Name already in use, please enter another name.")
                elif not name:
                    text_effect.slow_type("Cannot have a blank name, please write a name.")
                else:
                    break # Exit loop if name not duplicate
            else:
                # Default name is the player number set as a string.
                name = str(player_num)
                break # Need to break loop if we are not using names as using while True to loop until all names are unique.
            
        player = Player(number = player_num, name = name, cash = starting_cash)
        
        players.append(player)
          
    round_number = 1
    cards = ()
    
    ### START OF ROUNDS / TURNS / ACTIONS ###
    while round_number <= num_of_rounds:
        text_effect.divide_lines()
        print(f"ROUND {round_number} OF {num_of_rounds}")
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
            new_round(player) # wipe all players to ensure no issues going forward.
            # Exclude asking players how much to bet if we already know they do not have the money.
            if player.in_game:
                while True:
                    try:
                        bet = text_effect.slow_input(
                            f"How much is Player {player.name} betting (cash remaining: {text_effect.format_cash(player.cash)})? $"
                            )
                        bet = int(bet)
                        
                        if bet > player.cash:
                            print(f"Not enough funds, maximum available to Player {player.name} is {text_effect.format_cash(player.cash)}.")
                        elif bet < 1:
                            print("Must bet at least $1 or more")
                        else:
                            player.bet = bet
                            player.cash -= player.bet
                            break
                    except ValueError:
                        print(f"Invalid input, please enter a whole number between $1.00 and {text_effect.format_cash(player.cash)}.")
                        
        text_effect.sleep_line()
        
        # Deal cards to all active players and calculate scores
        for player in players:
            if player.active:
                # player.hand1 = [cards.pop() for _ in range(2)]
                # Comment out above line and use below if testing specific card combinations.
                player.hand1 = ["Ace of Tests", "Ace of Tests2"] #cards.pop()]
                player.score1 = winnings.calculate_score(player.hand1)
                # Comment out above line if you wish to test when players having specific score
                # player.score = 21
                if player.score1 == 21:
                    player.win1 = "Blackjack"
        
        # Used in multiple loops later on
        all_players_blackjack = all(player.win1 == "Blackjack" for player in players if player.active)
        
        # Deal cards to dealer and check for Blackjack            
        # dealer_hand = [cards.pop() for _ in range(2)]
        # Comment above line out and use the below if you manually wish to test cards
        dealer_hand = ["Ace of Tests", "King of Tests"] #cards.pop()]
        dealer_score = winnings.calculate_score(dealer_hand)
        # Comment out above line if you wish to test when dealer having specific score
        # dealer_score = 21
        dealer_upcard = dealer_hand[0].split()[0] # used later to allow insurance if allowed.
        winnings.does_dealer_have_blackjack(dealer_score)
        
        # Insurance check is completed before any other actions, including ending the game if dealer has blackjack
        if ins_active and dealer_upcard == "Ace":
            text_effect.slow_type(
                f"Dealer's upcard is the {dealer_hand[0]}, all players will be offered insurance." 
                )
            text_effect.sleep_line()
            for player in players:
                if player.active:
                    
                    # If player has blackjack then offer to "take even"
                    if player.win1 == "Blackjack":
                        text_effect.slow_type(
                            f"Player {player.name} has {player.hand1[0]} and {player.hand1[1]}. Blackjack!"
                        )
                        try:
                            while True:
                                action = text_effect.slow_input(
                                    "Would you like to 'take even'? (Y)es or (N)o? "
                                ).lower()
                                if action in ("yes", "y"):
                                    text_effect.slow_type(
                                            f"Player {player.name} wins {text_effect.format_cash(player.bet)} and is out for the rest of the round!"
                                        )
                                    player.win1 = "Take_even"
                                    # player.active = False
                                    break
                                elif action in ("no", "n"):
                                    text_effect.slow_type(
                                        f"Player {player.name} has opted to continue with their Blackjack."
                                    )
                                    if winnings.dealer_has_blackjack:
                                        player.win1 = "Push"
                                    break
                                else:
                                    text_effect.slow_type("Unknown command, please type 'yes' or 'no' to proceed.")
                        except Exception as e:
                            print(f"An error occurred: {e}")
                    
                    # If player doesn't have Blackjack then offer insurance if they can afford it.
                    else:        
                        insure_cost = float(player.bet / 2)
                        if insure_cost < player.cash:
                            try:
                                while True:
                                    action = text_effect.slow_input(
                                        f"Player {player.name}: pay {text_effect.format_cash(insure_cost)} to insure? (Y)es or (N)o: "
                                        ).lower()
                                    if action in ("yes", "y"):
                                        player.insure = True
                                        player.cash -= insure_cost
                                        if winnings.dealer_has_blackjack:
                                            player.win1 = "Insure"
                                        break
                                    elif action in ("no", "n"):
                                        break
                                    else:
                                        text_effect.slow_type("Unknown command, please type 'yes' or 'no' to proceed.")
                            except Exception as e:
                                print(f"An error occurred: {e}")
                        else:
                            text_effect.slow_type(f"Dealer's upcard is an ace, however you do not have enough funds to insure.")

            text_effect.sleep_line()
            
            # If dealer has blackjack then end game and show results
            if winnings.dealer_has_blackjack:
                text_effect.slow_type(f"Dealer has {dealer_hand[0]} and {dealer_hand[1]}. Blackjack!")
                for player in players:
                    if player.win1 != "Push":
                        player.win1 = "Dealer_blackjack"
                    
            # If dealer doesn't have blackjack then continue with normal game
            else:
                text_effect.slow_type(
                    "Dealer does not have blackjack. Insurance bets are lost and normal play resumes."
                )
            
            text_effect.sleep_line()
                
        # if we don't have insurance, then we can speed up the game
        elif ins_active == False:
            # If Dealer has Blackjack then skip normal game process as they can only match Blackjack to draw/push/tie.
            if winnings.dealer_has_blackjack == True:
                text_effect.slow_type(f"Dealer reveals hand: {dealer_hand[0]} and {dealer_hand[1]}\nDealer has Blackjack.")
                
                for player in players:
                    if player.active:
                        text_effect.slow_type(f"Player {player.name}'s hand: {player.hand1[0]} and {player.hand1[1]}")
                        if player.win1 == "Blackjack":
                            text_effect.slow_type(f"Player {player.name} has Blackjack!")
                            player.win1 = "Push"
                        else:
                            player.win1 = "Dealer_blackjack"
                        text_effect.divide_lines()
                
                if all_players_blackjack:
                    text_effect.slow_type("All participating players have Blackjack!")
                    text_effect.divide_lines()
                            
                text_effect.std_sleep()      
            
            # If all active players have Blackjack, then skip normal game process. We know dealer doesn't have Blackjack from "if" statement.
            elif all_players_blackjack and not winnings.dealer_has_blackjack:
                for player in players:
                    if player.active:
                        text_effect.slow_type(f"Player {player.name}'s hand: {player.hand1[0]} and {player.hand1[1]}")
                        player.win1 = "Blackjack"
                if num_of_players != 1:
                    text_effect.slow_type("All participating players have Blackjack. What about the dealer?")
                else:
                    text_effect.slow_type(f"Player {player.name} has Blackjack. What about the dealer?")
                text_effect.sus_sleep()
                text_effect.slow_type(
                    f"Dealer reveals hand: {dealer_hand[0]} and {dealer_hand[1]}\nDealer could not match, all players win!"
                    )
                text_effect.sleep_line()
        
        # Normal game play starts here  
        if (ins_active and winnings.dealer_has_blackjack == False) or winnings.dealer_has_blackjack == False:
            # Players have their turn
            for player in players:
                if player.active:
                    if player.cash >= player.bet:
                        player.dbl_avail = True
                        if player.hand1[0].split()[0] == player.hand1[1].split()[0]:
                            player.split_avail = True
                    text_effect.slow_type(f"Dealer's hand: {dealer_hand[0]} and unknown")
                    text_effect.slow_type(f"Player {player.name}'s hand: {player.hand1[0]} and {player.hand1[1]}")
                    
                    # Auto "stand" players on 21, otherwise ask what they would like to do.
                    if player.score1 == 21:
                        if player.win1 == "Take_even":
                            text_effect.slow_type(
                                f"Player {player.name} agreed to 'take even' earlier, ending their turn."
                            )
                        else:
                            text_effect.slow_type("Blackjack!")
                            player.win1 = "Blackjack"
                    else: 
                        text_effect.slow_type(f"Player {player.name}'s score: {player.score1}")
                            
                        player_actions(player, cards, charlie_active)
                            
                        if len(player.hand2) == 2 and player.hand2_stand == False:
                            player_actions(player, cards, charlie_active)
                    
                    text_effect.sleep_line()

            # Dealer plays if not all players are out and not all players have Blackjack
            all_players_out = all(not player.active for player in players)

            if all_players_out:
                text_effect.slow_type("All players are out.")
            elif not ins_active and all_players_blackjack and winnings.dealer_has_blackjack == False:
                continue
            else:
                text_effect.slow_type(f"Dealer reveals hand: {dealer_hand[0]} and {dealer_hand[1]}")
                # We only now advise if dealer has blackjack if insurance is active
                if ins_active and winnings.dealer_has_blackjack == True:
                    text_effect.slow_type("Dealer has Blackjack")
                    for player in players:
                        if player.active:
                            if player.win1 != "Blackjack":
                                player.win1 = "Dealer_blackjack"
                            else:
                                player.win1 = "Push"
                else:
                    if all_players_blackjack:
                        text_effect.slow_type("All active players have Blackjack, Dealer cannot match.")
                    else:
                        text_effect.slow_type(f"Dealer's score = {dealer_score}")

                        text_effect.std_sleep()                            

                        # Dealer must obtain new card until their score is above 16 (casino rules)
                        while dealer_score < 17 or (dealer_score == 17 and len(dealer_hand) == 2 and not s17_rule):
                            new_card = cards.pop()
                            dealer_hand.append(new_card)
                            dealer_score = winnings.calculate_score(dealer_hand)
                            text_effect.slow_type(f"Dealer receives: {new_card}\nDealer's new score: {dealer_score}")
                        
                        if dealer_score > 21:
                            text_effect.slow_type("Dealer has busted!")
                    
            text_effect.sleep_line() # Create divider when dealer has finished

        # Inform results and winnings / losses
        for player in players:
            if player.in_game:
                winnings.winner(dealer_score, player, hand = 1) # Prints results to screen
                win = winnings.player_payout(player, hand = 1)
                if win >= 0:
                    player.cash += win + player.bet + player.bet_dbl # must remember to give back their bet if they won
                if len(player.hand2) != 0:
                    winnings.winner(dealer_score, player, hand = 2)
                    win = winnings.player_payout(player, hand = 2)
                    if win >= 0:
                        player.cash += win + player.bet_split # must remember to give back their bet if they won
                    """we give back bet here and not within winnings.player_payout as the player_payout
                    def is used elsewhere to display how much they won which does not include the bet
                    itself.""" 
            
        text_effect.sleep_line() 
        
        if round_number < num_of_rounds:
            for player in players:
                if player.in_game:
                    if player.cash < 1:
                        text_effect.slow_type(
                            f"Player {player.name} doesn't have enough funds to bet! They are removed from the game!"
                            )
                        player.active = False 
                        player.in_game = False
                    else:
                        text_effect.slow_type(
                            f"Player {player.name} has {text_effect.format_cash(player.cash)} remaining."
                            )
                        player.active = True # Change back to true in case they busted this round but still have money for next round
                        
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