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
ALL_PLAYERS = "SELECT player_id, player_name, player_balance, player_points FROM Player"
DELETE_PLAYER = "DELETE FROM Player WHERE player_id = %s"
PLAYER_FULL_INFO = """SELECT 
    p.player_name,
    p.player_balance,
    p.player_points,
    COUNT(g.game_id) AS wins,
    (SELECT COUNT(*) FROM Hand h WHERE h.player_id = p.player_id) AS total_hands
FROM Player p
LEFT JOIN Game g ON g.winner_id = p.player_id
WHERE p.player_id = %s;
"""
#GAME QUERIES
START_GAME = "INSERT INTO Game () VALUES ()"
ADD_WINNER = "UPDATE Game SET winner_id = %s WHERE game_id = %s"
UPDATE_GAME_WINNER ="UPDATE Game SET winner_id = NULL WHERE winner_id = %s"
#HAND QUERIES
INSERT_HAND = "INSERT INTO Hand (game_id, player_id) VALUES (%s, %s)"
SELECT_HAND_ID = "SELECT hand_id FROM Hand WHERE game_id = %s AND player_id = %s ORDER BY hand_id DESC LIMIT 1"
DELETE_HAND = "DELETE FROM Hand WHERE player_id = %s"

#PLAYERHAND QUERIES
INSERT_CARDS_IN_HAND = "INSERT INTO PlayerHandCards (hand_id, card_id) VALUES (%s, %s)"

#PLAYER HAND CARDS
DELETE_PHC = "DELETE PHC FROM PlayerHandCards PHC JOIN Hand H ON PHC.hand_id = H.hand_id WHERE H.player_id = %s"

#PLAYS QUERIES
INSERT_PLAY = "INSERT INTO Plays (game_id, player_id, hand_id, play_action) VALUES (%s, %s, %s, %s)"
DELETE_PLAY = "DELETE FROM Plays WHERE player_id = %s"
#MULTIPLE TABLES
SELECT_GAME_INFO = """
SELECT 
    g.game_id, 
    p.player_name AS winner_name, 
    g.date_played,
    (
        SELECT COUNT(*) 
        FROM Plays 
        WHERE game_id = g.game_id
    ) AS total_actions
FROM Game g
JOIN Player p ON g.winner_id = p.player_id
WHERE g.winner_id IS NOT NULL
ORDER BY g.game_id DESC
"""

SELECT_GAME_DETAILS = """
SELECT 
    g.game_id, 
    p.player_name, 
    g.date_played
FROM Game g
JOIN Player p ON g.winner_id = p.player_id
WHERE g.game_id = %s
"""

SELECT_PLAY_DETAILS = """
SELECT 
    pl.play_action, 
    p.player_name, 
    pl.player_id, 
    pl.created_at
FROM Plays pl
JOIN Player p ON pl.player_id = p.player_id
WHERE pl.game_id = %s
ORDER BY pl.created_at
"""
SELECT_PLAYER_INFO = """
SELECT 
    p.player_id,
    p.player_name,
    (SELECT COUNT(*) FROM Game g WHERE g.winner_id = p.player_id) AS wins
FROM Player p
WHERE p.player_id = %s
"""

