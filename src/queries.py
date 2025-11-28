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