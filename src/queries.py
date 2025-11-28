#Contains queries used in the program

GET_ALL_CARDS = "SELECT card_id, card_value, suit FROM Cards"

GET_CARDS_BY_SUIT = """
    SELECT card_id, card_value, suit 
    FROM Cards 
    WHERE suit IN (%s, %s, %s, %s)
"""

INSERT_CARD = """
    INSERT INTO Cards (suit, card_value) 
    VALUES (%s, %s)
"""

GET_CARD_BY_ID = "SELECT card_id, card_value, suit FROM Cards WHERE card_id = %s"

#PLAYER QUERIES 
LOAD_PLAYER = "SELECT player_id, player_name, player_balance FROM Player WHERE player_id = %s"
INSERT_PLAYER = "INSERT INTO Player (player_name, player_balance) VALUES (%s, %s)"
UPDATE_PLAYER_BALANCE = "UPDATE Player SET player_balance = %s, player_points = %s WHERE player_id = %s"

#GAME QUERIES
START_GAME = "INSERT INTO Game () VALUES ()"
ADD_WINNER = "UPDATE Game SET winner_id = %s WHERE game_id = %s"

#HAND QUERIES
INSERT_HAND = "INSERT INTO Hand (game_id, player_id) VALUES (%s, %s)"

#PLAYERHAND QUERIES
INSERT_CARDS_IN_HAND = "INSERT INTO PlayerHandCards (hand_id, card_id) VALUES (%s, %s)"

#PLAYS QUERIES
INSERT_PLAY = "INSERT INTO Plays (game_id, player_id, play_action) VALUES (%s, %s, %s)"