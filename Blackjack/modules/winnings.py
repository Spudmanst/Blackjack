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
def dealer_has_blackjack(score):
    global dealer_blackjack
    if score == 21:
        dealer_blackjack = True
    else:
        dealer_blackjack = False
        
def player_payout(win, bet):
    blackjack_multiplier = float(options.variations["blackjack_payout"])
    charlie_multiplier = float(options.variations["charlie_payout"])
    if win == "Blackjack":
        return (bet * blackjack_multiplier)
    elif win == "Charlie":
        return (bet * charlie_multiplier)
    elif win == False or win == "Bust":
        return (-bet)
    elif win == "Push":
        return 0 
    else: # Last left is True
        return bet
    
def winner(dealer_score, player):
    if player.win == "Blackjack":
        return text_effect.slow_type(f"Player {player.name} wins with Blackjack! Win {text_effect.player_payout_format(player_payout(player.win, player.bet))}!")
    elif player.win == "Charlie":
        return text_effect.slow_type(f"Player {player.name} wins with 5-Card Charlie! Win {text_effect.player_payout_format(player_payout(player.win, player.bet))}!")
    elif player.win == "Dealer_blackjack":
        player.win = False # Need to change to false now to ensure it deducts money
        return text_effect.slow_type(f"Player {player.name} loses to dealer's Blackjack! Lose {text_effect.player_payout_format(player_payout(player.win, player.bet))}!")
    elif player.win == "Push":
        return text_effect.slow_type(f"Player {player.name} ties with Dealer's Blackjack! No Change!")
    elif player.win == "Bust":
        return text_effect.slow_type(f"Player {player.name} busted! Lose {text_effect.player_payout_format(player_payout(player.win, player.bet))}!")
    else:
        if dealer_score > 21:
            player.win = True
            return text_effect.slow_type(f"Player {player.name} wins as the Dealer busted! Win {text_effect.player_payout_format(player_payout(player.win, player.bet))}!")
        elif player.score > dealer_score and player.score <= 21:
            player.win = True
            return text_effect.slow_type(f"Player {player.name} wins with {player.score} vs the Dealer's {dealer_score}! Win {text_effect.player_payout_format(player_payout(player.win, player.bet))}!")
        elif player.score == dealer_score:
            player.win = "Push"
            return text_effect.slow_type(f"Player {player.name} ties with a score of {player.score}! No change!")
        else:
            player.win = False
            return text_effect.slow_type(f"Player {player.name} loses with {player.score} vs the Dealer's {dealer_score}! Lose {text_effect.player_payout_format(player_payout(player.win, player.bet))}!")
    