# POOCardGame
This is a POO project in which i will develop a poker-like game system using a POO architecture. This project can manage rounds and bets. This project also includes an interface made in TKinter and a database using MySQL to manage game history and game rules, aditionally it will keep some players information and their plays. 

# SQL
For this project i choose to use 6 tables 
1. Cards: this table will save all cards for the game. Cards include an ID, suit (Hearts, Spades,Clubs or Diamonds) and a value (A,1,2,3...)

2.Player: this table contains player information, an ID, name, date creation and balance.

3. Game: this table contains information about the played games, such as: ID, date played, and a winner (connecting to the player info using an ID)

4. Plays: This table contains a detail of the plays made by players during a game, it contains ID, game ID (connecting to a game), player id (connecting to a player), the action made by the player (Fold, check, rise, etc) and when was it made 

5. Hand: This table contains the information of a players hand, it contains: an ID, the game ID (connecting to game), player iD (connecting to player) and the datetime

6. PlayerHandCards contains the hand ID and card ID so we can know exactly which cards are in the hand