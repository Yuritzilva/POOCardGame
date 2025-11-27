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