from . import menus
from . import text_effect

def main():
    while True:
        action = text_effect.slow_input(
            "What would you like help on?\n"
            "1) The basics of Blackjack\n"
            "2) The variations\n"
            "3) Back to main menu\n"
            )
        
        if action in "1":
            text_effect.divide_lines()
            text_effect.slow_type("THE BASICS")
            text_effect.divide_lines()
            text_effect.slow_type(
                "The object of the game is to beat the dealer by having a higher score "
                "without exceeding 21 points.\n"
                "The value written on the card is the score that card provides (i.e., "
                "the 5 of hearts awards you 5 points).\n"
                "Picture cards (i.e., Jack, Queen and King) are all worth 10 points each.\n"
                "Ace cards are unique as they can be either 1 or 11 points. Aces are generally "
                "considered 11 points unless the hand 'busts' (i.e., exceeds 21 points) "
                "at which point the Ace is considered 1 point.\n"
                "Multiple Aces in a hand may be considered different values, e.g., Ace "
                "+ Ace + 5 = 17. First Ace is 11 points, second Ace is 1 point."
            )
            text_effect.sleep_line()
            text_effect.sus_sleep()
            text_effect.slow_type(
                "Each player and the dealer are dealt 2 cards each to start. The players "
                "will take their turns before the dealer. If the player has an Ace and a card "
                "with the value 10 (10, Jack, Queen, King) then they have Blackjack. The dealer "
                "cannot beat Blackjack but they can match it. The same can be said if the dealer "
                "has Blackjack, the player can only tie the result. Blackjack is the best hand "
                "a player (or the dealer) can obtain."
            )
            text_effect.sleep_line()
            text_effect.sus_sleep()
            text_effect.slow_type(
                "If the player doesn't have Blackjack, they will be presented with some options:\n"
                "'Hit' - to be given a new card to add to their hand and increase their points.\n"
                "'Stand' - to stick or stop receiving new cards and end their turn.\n"
                "'Split' - if both starting cards are the same value, the player may pay their bet "
                "again to split the cards and create two hands to play from. The player will "
                "resolve each hand separately.\n"
                "'Double' - the player will pay their bet again to receive one additional card "
                "and immediately end their turn straight after regardless of the result."
            )
            text_effect.sleep_line()
            text_effect.sus_sleep()
            text_effect.slow_type(
                "Once all players have ended their turn, either manually or by busting "
                "(exceeding 21 points), the dealer will reveal their hand. If the dealer has a score "
                "less than 17, they will provide themselves with another card, otherwise they will "
                "stand. The dealer can bust by exceeding 21 points. Once the dealer has completed "
                "their turn, the results for all players will be determined."
            )
            text_effect.divide_lines()
            main()
        elif action in "2":
            text_effect.slow_type("WIP 2")
            main()
        elif action in ("3", "e"):
            text_effect.divide_lines
            menus.main_menu()
        elif action in "r":
            main()
        else:
            text_effect.slow_type("Unknown command, please type a number corresponding to the help you require.")