from . import menus
from . import text_effect

def main():
    while True:
        action = text_effect.slow_input(
            "What would you like help on?\n"
            "1) The basics of Blackjack\n"
            "2) The terminology\n"
            "3) Back to main menu\n"
            )
        text_effect.divide_lines()
        
        if action in "1":
            text_effect.slow_type("THE BASICS")
            text_effect.divide_lines()
            text_effect.slow_type(
                "The object of the game is to beat the dealer by having a higher score "
                "without exceeding 21 points.\n"
                "The value written on the card is the score that card provides (i.e., "
                "the 5 of hearts awards you 5 points).\n"
                "Picture cards (i.e., Jack, Queen and King) are all worth 10 points each "
                "apart from an Ace.\n"
                "Ace cards are unique as they can be either 1 or 11 points. Aces are generally "
                "considered 11 points unless the hand 'busts' (i.e., exceeds 21 points) "
                "at which point the Ace is considered 1 point.\n"
                "Multiple Aces in a hand can have different values, e.g., Ace "
                "+ Ace + 5 = 17. One Ace is 11 points, the other Ace is 1 point."
            )
            text_effect.divide_and_read()
            text_effect.slow_type(
                "After placing their bets, each player and the dealer are dealt 2 cards each to start "
                "The players will take their turns before the dealer. If the player has an Ace and "
                "a card with the value 10 (10, Jack, Queen, King) then they have Blackjack. The dealer "
                "cannot beat Blackjack but they can match it. The same can be said if the dealer "
                "has Blackjack, the player can only tie the result. Blackjack is the best hand "
                "a player, or the dealer, can obtain. If the dealer has Blackjack then this "
                "will be revealed before any actions are taken."
            )
            text_effect.divide_and_read()
            text_effect.slow_type(
                "If the player or dealer doesn't have Blackjack then the players will be presented "
                "with some options:\n"
                "'Hit' - to be given a new card to add to their hand and increase their points.\n"
                "'Stand' - to stick or stop receiving new cards and end their turn.\n"
                "'Split' - if both starting cards are the same value, the player may pay their bet "
                "again to split the cards and create two hands to play from. The player will "
                "resolve each hand separately.\n"
                "'Double' - the player will pay their bet again to receive one additional card "
                "and immediately end their turn straight after regardless of the result."
            )
            text_effect.divide_and_read()
            text_effect.slow_type(
                "Once all players have ended their turn, either manually or by busting "
                "(exceeding 21 points), the dealer will reveal their hand. If the dealer has a score "
                "less than 17, they will provide themselves with more cards until they have 17 or " 
                "more ponts, at which point they will stand (i.e. stick). The dealer can also bust."
                "Once the dealer has completed their turn, the results for all players will be determined."
            )
            text_effect.divide_and_read()
            text_effect.slow_type(
                "If a player beats the dealer, their bet is return to them plus the dealer will "
                "pay them an equal amount, this is a 1:1 ratio. For example, if you win a $10 bet, "
                "you will receive your $10 back plus an additional $10, totalling $20.\n"
                "If the player beats the dealer with a Blackjack, their bet is returned plus 1.5 "
                "times the original bet, this is a 3:2 ration. For example, if you win a $10 bet, "
                "you will receive your $10 back plus an addtional $15, totalling $25.\n"
                "If the player draws/ties with the dealer, their bet is returned and nothing more. "
                "This is known as a 'push'." 
                "If the player loses to the dealer then they will lose their bet."
            )
            text_effect.divide_and_read()
            main()
            
        elif action in "2":
            text_effect.slow_type("THE TERMINOLOGY")
            text_effect.divide_lines()
            text_effect.slow_type("STANDARDS")
            text_effect.divide_lines()
            text_effect.slow_type(
                "BLACKJACK (or Natural) - a two-card hand totaling 21, consisting of an Ace and a 10-value "
                "card (10, Jack, Queen, King).\n"
                "HIT - to request an additional card from the dealer.\n"
                "STAND - to keep the current hand and not take any more cards.\n"
                "BUST - When a hand total exceeds 21, resulting in an automatic loss.\n"
                "PUSH - a tie between the player and the dealer."
            )
            text_effect.divide_and_read()
            text_effect.slow_type("ADVANCE")
            text_effect.divide_lines()
            text_effect.slow_type(    
                "SPLIT - if a player's first two cards are the same rank (e.g. two 8s), they can place an "
                "additional bet equal to the original to split them into two separate hands which are then "
                "played independently. It's important to note that players will not benefit from a higher payout "
                "if you obtain Blackjack after splitting and they may not 'double' after splitting either.\n"
                "DOUBLE (or Double Down) - a player doubles their inital bet after receiving the first two cards "
                "and receives only one additional card.\n"
                "INSURANCE - a side bet offered to players if the dealer's upcard is an Ace. The player can "
                "wager half their original bet, and if the dealer has a blackjack, the insurance pays 2:1. "
                "This means that even though the player loses their orignal bet, the win on the insurance "
                "will cover their losings, therefore the player does not lose any money. If the dealer doesn't "
                "have blackjack then the side bet is lost and the game continues as normal.\n"
                "TAKE EVEN - offered to players who have Blackjack when the dealer's upcard is an Ace and the " 
                "insurance option is turned on. If the player accepts then they will win based on a 1:1 ration. "
                "Benefit is the player wins money if the dealer has Blackjack. The drawback is the player does not "
                "win the standard 3:2 payout if the dealer did not have Blackjack.\n"
                "5 CARD CHARLIE - if a player obtains 5 cards without busting then they will automatically "
                "beat the dealer (unless the dealer has BLACKJACK). The specifics of this rule differs from "
                "casino to casino and is uncommon to find as this benefits the player. "
                "Not all Blackjack or casino terminology will be covered in this, however you will be provided "
                "with any used within this game and their explanations."
            )
            text_effect.divide_and_read()
            main()
            
        elif action in ("3", "e"):
            text_effect.divide_lines
            menus.main_menu()
            
        elif action in "r":
            main()
            
        else:
            text_effect.slow_type("Unknown command, please type a number corresponding to the help you require.")