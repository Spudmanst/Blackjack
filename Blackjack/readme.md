# BLACKJACK

#### Video Demo: https://youtu.be/MFphGRa-kf0

#### Description:

A simple game of Blackjack (a.k.a. 21s). Each player is dealt 2 cards from a deck and add the ranks of the cards, i.e. A, 2, 3... J, Q, K, to calculate their score. The objective is to get a score as close to 21 without exceeding it. Picture cards are valued at 10 points, Ace is worth 1 or 11 points depending on the situation. If the player has an Ace and a card worth 10 (10, J, Q or K) with their first two cards then they have "Blackjack". 

I have designed this to be more "casino style" of gameplay where all players are playing against the dealer and bet each round in an attempt to make money. 

## Using Python

The main reason I opted to use Python over the other languages we were taught was because I struggled with Python the most and wanted to spend more time learning it. I am sure I could have acomplished this use C however, I will admit, Python did seem the most appealing language to use in view of its ease of use (higher level programming) and not needing to be concerned with memory allocation (malloc and free).

## Files

Originally all the code was typed into one file however as I progressed with expanding and improving the program, it became apparent that the file was becoming difficult to nagivate, making it harder to isolate specific tasks/functions that needed amending or reviewing. I therefore made the choice to seperate out aspects of the coding to help allievate this issue. Below will be a brief on each file and what they are for.

### Blackjack.py

Sole purpose is where the program would be initiaed from. Originally I was considering implimenting the main menu into this file but opted against it purely as I was unsure how much was going into the menus.py file. If I had opted to focus more time into the design and structure of the program, then I would have likely merged Blackjack.py and menus.py into one file. 

### change_log.txt

I was not acustomed to Github and therefore did not fully appreciate it's capabilities when I started this project and, because of this, I wanted to ensure there was a list of all changes made to the code so I could easily review histocial changes if I ever needed to. Although I now know that Github is extremely useful for documenting changes (if done correctly) and being able to revert back to old code if required, I would still keep this file for two reasons:
1. My own benefit
2. Game developers usually publish a list of changes when updates/patches are completed to a game. Considering this is a game, I felt best to follow suit.

### notes.txt

I was previously familiar with Blackjack however I have never been to a casino. I am aware that casinos have slightly different rules but I had no clue what they were. I used this file to draft out my original thoughts and knowledge of the game to help my mental preparations of what I needed to do to get the game working and the code in some sort of logical order. I expanded on these notes as and when I researched more aspects of Blackjack within casinos to help serve as a quick reference if I ever needed it. In hindsight, I should have spent more time on this file and potentially called it "design document" as this could have helped with issues I encountered during the coding of this game.

### todo.txt

As the file expanded I found my mind would wonder from one task to the next and slowly getting mixed up in what I had done or was in the middle of doing. This was especially prevelant during testing as I would work on "item a", find an issue during a test, go and fix the issue, forget what I was doing with "item a". I would use this as a live file on the day I was coding to:
- Make a note of the objective for the day
- Write down current project / aspect of the code I was working on and why
- Make notes of issues incurred or found during testing or reviewing
- Write my ideas on what I could do to expand the game further.
- Mark ideas as completed when reviewed and tests.
- Mark ideas as scrapped if I felt best not to proceed for now however wanted the notes for future potential expansions

This file was perhaps the most used file as it helped keep my thoughts on track and ensure I completed my project without constantly getting stuck with "What was I doing?" thoughts after each test/review of coding and logic.

### modules/__init__.py

Required file to ensure project worked as expected.

### modules/advice.py

I wanted to provide a place for users to be able to get some basic information of Blackjack and how to play without the need to come out of the program.

### modules/menus.py

As mentioned before, in hindsight this could have been merged into the Blackjack.py file. A simple little menu that the users are greeted with where they can start the game, check out the options, obtain a bit of help on the game, or quit the program.

### modules/options.py

This is where users review the current settings for the game or make changes to match their preferences. Users can change a number of factors such as:
- Increasing / Decreasing how much they win for getting Blackjack
- Enabling 5 Card Charlie variation to be possible.
- Allow for insurance to be available when the dealer's up turned card is an Ace
- How many decks of cards are being used.

In view of casinos having their own rules, I figured players of this game should have the same ability. One of the variations I was not expecting to add was the number of decks being used. I thought the dealer must shuffle a deck of cards often however while researching cainso and Blackjack, I found that they use multiple packs to prevent the need for constant shuffling however they also needed to ensure that they shuffled enough to minimise the chances of someone "counting cards". At this point I figured I would try to design the game in a way that would allow users to attempt to count cards but try and keep within the boundaries that casinos would do.

### modules/playing_cards.py

This file is purely used to create one deck of cards. It was originally within the "the_game.py" file however I figured I shouldn't need to touch this aspect of the code once it was working correctly and therefore moved it into it's own file to prevent any accidential alterations.

### modules/text_effect.py

One of the main problems I had was how the text was being printed instantly to the screen, I felt this was too disorientating from the players perspective as you would suddenly be greeted with a large block of text which could also push text off the screen you were reading at the time. I knew there would be a way to slow down the text but unsure how, so after a quick Google and assistance from ChatGPT.com, I was able to make a function to slow down how quickly the text appears on the screen and gives the illusion that the game is typing text. This file contains different functions that help with the presentation during the game play, allowing for pausing, phyiscal line breaks and slow typing to happen within the game itself. There are also a couple of format functions within the file too that are used in multiple places within other parts of the code.

### modules/the_game.py

This is the main file for the game as it holds all the logic to allow the game to play out, as well as the Player class to inform the program how to construct Player information for later use. 

The code will ask for the number of players and whether users wish to give them names or not, then proceed to load values from the variations (within options) which affects future logic as well as help build the Player information, e.g. the amount of starting cash can be altered within the options, which needs to be imported to this file.

Once the players and the settings are ready, the game will play out, asking players how much they wish to bet, dealing each player and the dealer two cards, informing the player what the dealer's upturned card is and presenting them with options. The game will automatically end a player's turn if they reach 21 or have Blackjack and the game will also understand whether to end the game early because the dealer has Blackjack or to wait and provide players with the option to insure (if this option has been turned on) and act accordingly.

If the dealer doesn't have Blackjack and all player's turns are completed, the dealer will complete their turn as per casino rules of Standing on 17 or above If the dealer has a score of exactly 17 and one of the cards is an Ace being counted as 11 points, this is known as having a soft score of 17 as the Ace acts as a buffer if you decide to hit and bust since the Ace can then be counted as 1 point, not 11 and therefore prevent you from busting. If the dealer has a soft score of 17 then it will "hit" instead of "standing" when s17 == False.

Once the dealer has concluded their turn, the player's and dealers scores are fed to a different file (win_check.py) to calculate who has beaten the dealer (or not). If a player has won then they are awarded their winnings and their bet is returned to them.

The above process continues until all rounds have been concluded, then the final score board is displayed, showing the players in decending order, i.e. the winning is printed first.

#### Design decisions for modules/the_game.py

It may be odd that I have added a limit to the max number of players when theorectically you could have a much higher "MAX_PLAYERS" number, however I have purposely set it to 7 as research indicated to me that only 7 people could sit round a Blackjack table in the casino. I figured if I wanted to expand on this program in the future, potentially with graphics, then I should design the game for a max of 7 players. 

I felt that having the Players details and information within a class was the best approach in view of being able to quickly expand on new variables as and when required, as well as how easy it is to have the system create new values based on the number of people playing. 

As the code was expand with more variations and logic, the more indentations was required within running of the game which made the code harder to read / understand.  To help mitigate this issue, I created a couple of helper functions, such as "new_round(player)" and "player_actions(player, cards, charlie_on)", then inserted these into the core game logic. In hindsight, I do feel like I should have thought about adding more "helper functions" sooner to further help with this. 

### modules/win_check.py

Originally this file was purely used to check whether a player had beaten the dealer then display a message in relation to it, however it expanded further over time. If I needed to just check the score for any reason, this was left within the main "the_game.py" file, however if the hand needed reviewing, e.g. 5 Card Charlie, I decided to move the logic into this section as well to help keep the main code cleaner. This file also does calculate the winnings of a player if they do win but it does not return the winnings to their overall cash, this has been left to the main code to complete in view of specific senarios that could occur. 