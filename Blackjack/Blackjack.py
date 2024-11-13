# Blackjack version alpha 3.0.0pre-g

from modules import menus

def main():

    print(r"""
    ____  _            _        _            _    _
    |  _ \| |          | |      | |          | |  | |
    | |_) | | __ _  ___| | __   | | __ _  ___| | _| |
    |  _ <| |/ _` |/ __| |/ /   | |/ _` |/ __| |/ / |
    | |_) | | (_| | (__|   < |__| | (_| | (__|   <|_|
    |____/|_|\__,_|\___|_|\_\____/ \__,_|\___|_|\_(_)
                                                    """)

    while True:
        menus.main_menu()

if __name__ == "__main__":
    main()