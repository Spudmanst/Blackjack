from . import advice
from . import options
from . import text_effect
from . import the_game
import sys

def main_menu():
    while True:
        action = text_effect.slow_input("What would you like to do? (P)lay, (O)ptions, (H)elp, (E)xit: ").lower()

        if action in ("play", "p"):
            text_effect.divide_lines()
            the_game.start_game()
        elif action in ("options", "option", "o"):
            options.main()
        elif action in ("help", "h"):
            advice.main()
        elif action in ("exit", "e"):
            print("Exiting game.")
            text_effect.divide_lines()
            sys.exit()
        else:
            print("Unknown command, type 'play', 'options', 'help' or 'exit'.")