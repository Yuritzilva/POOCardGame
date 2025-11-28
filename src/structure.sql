
CREATE TABLE IF NOT EXISTS Player (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(50) NOT NULL,
    player_balance DECIMAL(10,2) DEFAULT 100.00,
    player_points DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS Game (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    date_played DATETIME DEFAULT CURRENT_TIMESTAMP,
    winner_id INT,
    FOREIGN KEY (winner_id) REFERENCES Player(player_id)
);


CREATE TABLE IF NOT EXISTS Cards (
    card_id INT AUTO_INCREMENT PRIMARY KEY,
    suit VARCHAR(20),
    card_value VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Hand (
    hand_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT,
    player_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);

CREATE TABLE IF NOT EXISTS PlayerHandCards (
    hand_id INT,
    card_id INT,
    PRIMARY KEY (hand_id, card_id),
    FOREIGN KEY (hand_id) REFERENCES Hand(hand_id),
    FOREIGN KEY (card_id) REFERENCES Cards(card_id)
);

CREATE TABLE IF NOT EXISTS Plays (
    play_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT,
    player_id INT,
    hand_id INT,
    play_action VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (hand_id)   REFERENCES Hand(hand_id)
);
