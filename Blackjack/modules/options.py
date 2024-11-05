from . import menus
from . import text_effect

default_variations = {
    "blackjack_payout" : 1.5,
    "5_card_charlie" : False,
    "charlie_payout" : 1,
    "num_of_packs" : 2,
    "insurance" : False,
    "s17" : True,
    "resplitting" : False,
    "double_after_split" : False,
    "reno_rule" : False,
    "dealer_wins_ties" : False
}

variations = {
    "blackjack_payout" : 1.5,
    "5_card_charlie" : False,
    "charlie_payout" : 1,
    "num_of_packs" : 2,
    "insurance" : False,
    "s17" : True,
    "resplitting" : False,
    "double_after_split" : False,
    "dealer_wins_ties" : False
}

def print_settings():
    text_effect.slow_type("Current Settings:")
    for key, value in variations.items():
        text_effect.slow_type(f"{key} : {value}")

def reset_to_defaults(settings, defaults):
    settings.clear()
    settings.update(defaults)

def main():
    text_effect.slow_type("From here you can alter variations of the game.")
    while True:
        action = text_effect.slow_input(
            "What would you like to do?:\n"
            "1) View current settings\n"
            "2) Alter settings\n"
            "3) Return to main menu.\n"
            "Input: "
            )
        text_effect.divide_lines()
        if action in "1":
            print_settings()
            text_effect.divide_and_read()
            main()
        elif action in "2":
            while True: 
                action = text_effect.slow_input(
                    "What setting would you like to change:\n"
                    "1) Blackjack payout\n"
                    "2) 5 Card Charlie\n"
                    "3) Charlie payout\n"
                    "4) Number of packs\n"
                    "5) Insurance\n"
                    "6) S17 or H17\n"
                    "7) Resplitting\n"
                    "8) Double allowed after splitting\n"
                    "9) Dealer wins ties\n"
                    "You can respond with 'default' if you wish to go back to the orignal settings.\n"
                    "Alternatively you can type 'exit' to leave this menu.\n" 
                    "Input: "
                    )
                text_effect.divide_lines()
                
                if action in "1":
                    text_effect.slow_type("This is how much you will earn for winning with Blackjack, default is 1.5.")
                    while True:
                        action = text_effect.slow_input("Please advise of a multiplier between 1 & 10: ")
                        try:
                            action_float = float(action) # action is currently string so change to float
                            if 1 <= action_float <= 10:
                                if action.count(".") == 0 or len(action.split(".", 1)[1]) <= 1: # check for . and if so check only 1 number after .
                                    variations["blackjack_payout"] = action_float
                                    text_effect.slow_type(f"Blackjack payout is now {variations["blackjack_payout"]}")
                                    text_effect.divide_and_read()
                                    break
                                else:
                                    text_effect.slow_type("Invalid input. Please enter a number with up to 1 decimal place.")
                            else:
                                text_effect.slow_type("Invalid input. Please enter a number between 1.0 and 10.")
                        except ValueError:
                            text_effect.slow_type("Invalid input. Please enter a valid number between 1.0 and 10.")
                        
                elif action in "2":
                    text_effect.slow_type(
                        "You can enable 5 Card Charlie. If the player reaches 5 cards without busting "
                        "then they automatically stick. 5 Card Charlie is better than 21 but worse than "
                        "Blackjack. This rule is specific to the player. Default is False."
                    )
                    while True:
                        action = text_effect.slow_input("Would you like 5 Card Charlie on? Yes or no: ").lower()
                        if action in ("yes", "y"):
                            variations["5_card_charlie"] = True
                            break
                        elif action in ("no", "n"):
                            variations["5_card_charlie"] = False
                            break
                        else:
                            text_effect.slow_type("Unknown command, please type Yes or No.")
                        
                    text_effect.slow_type(f"Setting for 'Is 5 Card Charlie active?' is set to {variations["5_card_charlie"]}.")
                    text_effect.divide_and_read()
                            
                elif action in "3":
                    text_effect.slow_type("This is how much you will earn for winning with 5 Card Charlie, default is 1.")
                    while True:
                        action = text_effect.slow_input("Please advise of a multiplier between 1 & 5: ")
                        try:
                            action_float = float(action)
                            if 1 <= action_float <= 5:
                                if action.count(".") == 0 or len(action.split(".", 1)[1]) <= 1:
                                    variations["charlie_payout"] = action_float
                                    text_effect.slow_type(f"Payout for 5 Card Charlie is now {variations["charlie_payout"]}.")
                                    text_effect.divide_and_read()
                                    break
                                else:
                                    text_effect.slow_type("Invalid input. Please enter a number with up to 1 decimal place.")
                            else:
                                text_effect.slow_type("Invalid input. Please enter a number between 1.0 and 5.")
                        except ValueError:
                            text_effect.slow_type("Invalid input. Please enter a valid number between 1.0 and 5.")
                            
                elif action in "4":
                    text_effect.slow_type(
                        "This is how many deck of cards are used to generate the full pile the dealer pulls from. "
                        "Default is 1."
                    )
                    while True:
                        action = text_effect.slow_input("How many decks would you like to use between 1 and 8: ")
                        try:
                            if 1 <= int(action) <= 8:
                                variations["num_of_packs"] = int(action)
                                text_effect.slow_type(f"Number of packs being used is now {variations["num_of_packs"]}.")
                                text_effect.divide_and_read()
                                break
                        except ValueError:
                            text_effect.slow_type("Invalid input. Please enter a whole number between 1 and 8.")
                            
                elif action in "5":
                    text_effect.slow_type(
                        "Allows the option to insure if the dealer has a chance of Blackjack. "
                        "Players may pay half their bet to insure. If a player insurers and the dealer has Blackjack "
                        "then they will receive their insure money and original bet back. If the dealer doesn't have "
                        "Blackjack then the insured money is lost regardless, even if the player beats the dealer later. "
                        "Default is off."
                    )
                    while True:
                        action = text_effect.slow_input("Would you like Insurance on? Yes or no: ").lower()
                        if action in ("yes", "y"):
                            variations["insurance"] = True
                            break
                        elif action in ("no", "n"):
                            variations["insurance"] = False
                            break
                        else:
                            text_effect.slow_type("Unknown command, please type Yes or No.")
                    
                    text_effect.slow_type(f"Setting for 'Is insurance allowed?' is set to {variations['insurance']}.")
                    text_effect.divide_and_read()
                            
                elif action in "6":
                    text_effect.slow_type(
                        "S17 or H17 refers to how the dealer will act when they an Ace in their hand and reach a score of 17. "
                        "S17 means the dealer will 'stand', whereas H17 means they will 'hit'. Default is S17."
                    )
                    while True:
                        action = text_effect.slow_input("Which rule would you like? (S)17 or (H)17: ").lower()
                        if action in "s":
                            variations["s17"] = True
                            break
                        elif action in "h":
                            variations["s17"] = False
                            break
                        else:
                            text_effect.slow_type("Unknown command, please type S or H.")
                    
                    text_effect.slow_type(f"Setting for 'Use s17?' is set to {variations["s17"]}.")
                    text_effect.divide_and_read()
                        
                elif action in "7":
                    text_effect.slow_type(
                        "Resplitting allows the player to split again if after splitting, "
                        "the first two cards in a hand are the same again. Default is off."
                    )
                    while True:
                        action = text_effect.slow_input("Would you like to allow resplitting? Yes or No: ").lower()
                        if action in ("yes", "y"):
                            variations["resplitting"] = True
                            break
                        elif action in ("no", "n"):
                            variations["resplitting"] = False
                            break
                        else:
                            text_effect.slow_type("Unknown command, please type Yes or No.")
                    
                    text_effect.slow_type(f"Setting for 'Is replitting allowed?' is set to {variations['resplitting']}.")
                    text_effect.divide_and_read()
                        
                elif action in "8":
                    text_effect.slow_type(
                        "'Double after split' is where a player is allowed to 'double' after splitting. "
                        "Default is off."
                    )
                    while True:
                        action = text_effect.slow_input("Would you like to allow double after splitting? Yes or No: ")
                        if action in ("yes", "y"):
                            variations["double_after_split"] = True
                            break
                        elif action in ("no", "n"):
                            variations["double_after_split"] = False
                            break
                        else:
                            text_effect.slow_type("Unknown command, please type Yes or No.")
                    
                    text_effect.slow_type(f"Setting for 'Can double after splitting?' is set to {variations["double_after_split"]}.")
                    text_effect.divide_and_read()
                        
                elif action in "9":
                    text_effect.slow_type("'Dealer wins ties' does exactly as it states. Default is off.")
                    action = text_effect.slow_input("Would you like the dealer to win ties? Yes or No: ")
                    while True:
                        if action in ("yes", "y"):
                            variations["dealer_wins_ties"] = True
                            break
                        elif action in ("no", "n"):
                            variations["dealer_wins_ties"] = False
                            break
                        else:
                            text_effect.slow_type("Unknown command, please type Yes or No.")
                        
                    text_effect.slow_type(f"Setting for 'dealer wins ties' is set to {variations['dealer_wins_ties']}.")
                    text_effect.divide_and_read()
                    
                elif action in ("default", "d"):
                    reset_to_defaults(variations, default_variations)
                    
                elif action in ("exit", "e"):
                    main()
                else: 
                    text_effect.slow_type("Unknown command, please type a number corresponding to the action you wish to take.")
            
        elif action in "3":
            text_effect.divide_lines()
            menus.main_menu()
        else:
            text_effect.slow_type("Unknown command, please type a number corresponding to the action you wish to take.")