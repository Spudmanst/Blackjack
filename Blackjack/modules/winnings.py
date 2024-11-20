from . import options
from . import playing_cards
from . import text_effect

# Prep to check for Aces If player "bust" and change score
def calculate_score(hand):
    score = sum(playing_cards.scores[card.split()[0]] for card in hand)
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
    
# Gobal variable used if dealer has Blackjack to skip large parts of coding. 
def does_dealer_have_blackjack(score):
    global dealer_has_blackjack
    if score == 21:
        dealer_has_blackjack = True
    else:
        dealer_has_blackjack = False

def player_payout(player, hand):
    if hand == 1:
        x = player_payout_logic(player.win1, player.bet, player.bet_dbl)
    else:
        x = player_payout_logic(player.win2, player.bet, 0)
        
    x = float(x)

    return x
        
def player_payout_logic(win, bet, additional_bet):
    blackjack_multiplier = float(options.variations["blackjack_payout"])
    charlie_multiplier = float(options.variations["charlie_payout"])
    dealer_wins_ties = options.variations["dealer_wins_ties"]
    if win == "Blackjack":
        return (bet * blackjack_multiplier)
    elif win == "Charlie":
        return (bet * charlie_multiplier)
    elif win == False or win == "Bust" or (win == "Push" and dealer_wins_ties):
        return (-bet - additional_bet)
    elif win == "Push":
        return 0 
    elif win == "Insure" :
        return (bet * 0.5) # This returns the insurance cost
    else: # Last left is True, "split_blackjack" (which does not get the
        # Blackjack payout) and "take_even". 
        return bet + additional_bet
    
def winner(dealer_score, player, hand):
    dealer_wins_ties = options.variations["dealer_wins_ties"]
    result = player.win2 if hand == 2 else player.win1
    score = player.score2 if hand == 2 else player.score1
    win = None
    win_amount = text_effect.player_payout_format(player_payout(player, hand))
    
    if result == "Blackjack":
        mgs =  f"Player {player.name} wins with Blackjack! Win {win_amount}!"
    
    elif result == "Charlie":
        mgs = f"Player {player.name} wins with 5-Card Charlie{" with their second hand" if hand == 2 else ""}! Win {win_amount}!"
    
    elif result == "Dealer_blackjack" and player.insure == False:
        win = False # Don't think this is needed anymore, need to test
        mgs = f"Player {player.name} loses to dealer's Blackjack{" with their second hand" if hand == 2 else ""}! Lose {win_amount}!"
        
    elif result == "Dealer_blackjack" and player.insure == True:
        win = "Insure" # Need to ensure they recover their bet and insurance money
        mgs = f"Player {player.name} loses to dealer's Blackjack but recover their bet and insurance costs!"
        
    elif result == "Push":
        mgs = ((f"Player {player.name} ties with Dealer's Blackjack{" with their second hand" if hand == 2 else ""}! ")
        + (f"Lose {win_amount}!" if dealer_wins_ties else "No Change!"))
    
    elif result == "Bust":
        mgs = f"Player {player.name} busted{" with their second hand" if hand == 2 else ""}! Lose {win_amount}!"
        
    elif result == "Take_even":
        mgs = f"Player {player.name} decided to 'take even' and therefore wins {win_amount}!"
    
    elif dealer_score > 21:
        win = True
        mgs = f"Player {player.name} wins as the Dealer busted{" with their second hand" if hand == 2 else ""}! Win {win_amount}!"
    
    elif score > dealer_score and score <= 21:
        win = True
        mgs = f"Player {player.name} wins with {score} vs the Dealer's {dealer_score}{" with their second hand" if hand == 2 else ""}! Win {win_amount}!"
    
    elif score == dealer_score:
        win = "Push"
        mgs = ((f"Player {player.name} ties with a score of {score}{" with their second hand" if hand == 2 else ""}! ")
        + (f"Lose {win_amount}!" if dealer_wins_ties else "No Change!"))
    
    else:
        win = False
        mgs = f"Player {player.name} loses with {score} vs the Dealer's {dealer_score}{" with their second hand" if hand == 2 else ""}! Lose {win_amount}!"

    if win != None:
        if hand == 2:
            player.win2 = win
        else:
            player.win1 = win
    
    return text_effect.slow_type(mgs)