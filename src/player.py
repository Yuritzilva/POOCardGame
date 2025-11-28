class Player:
    def __init__(self, id_, name, initial_balance,  points = 0.00, is_bot=False):
        self.id = id_
        self.name = name
        self.balance = initial_balance
        self.points = points
        self.folded = False 
        self.is_bot = is_bot
        self.hand = []  
        self.current_bet = 0  
        self.total_bet = 0 
    
    @classmethod
    def get_player(cls, player_id):
        """load player from DB"""
        from db_connection import get_conn
        from queries import LOAD_PLAYER
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(LOAD_PLAYER, (player_id,))
            row = cur.fetchone()
            if row:
                return cls(row[0], row[1], float(row[2]))
            return None
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def set_player(cls, name, initial_balance=100.00):
        """create new player"""
        from db_connection import get_conn
        from queries import INSERT_PLAYER
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(INSERT_PLAYER,(name, initial_balance))
            conn.commit()
            player_id = cur.lastrowid
            return cls(player_id, name, initial_balance)
        finally:
            cur.close()
            conn.close()
    
    def add_winnings(self, amount, hand_value):
        """Add winning stats to the player"""
        self.balance += amount 
        self.points += hand_value 
        #print(f" === WINNER === \n {self.name} \n === BALANCE === \n {amount} \n === POINTS === \n {hand_value} \n")
        self._update_balance_in_db()

    def place_bet(self, amount):
        """Make bet"""
        if amount > self.balance:
            amount = self.balance  # All-in
            self.all_in = True
        
        self.balance -= amount
        self.current_bet += amount
        self.total_bet += amount

        self._update_balance_in_db()
        return amount
    
    def fold(self):
        """Fold"""
        self.folded = True
        self.current_bet = 0
    
    def reset_for_new_round(self):
        """Reset for new round"""
        self.hand = []
        self.current_bet = 0
        self.folded = False
        self.all_in = False
        self.total_bet = 0
    
    def receive_card(self, card):
        """Recieve cards"""
        if len(self.hand) < 2:
            self.hand.append(card)
        else:
            print(f"{self.name} already has 2 cards")
    
    def _update_balance_in_db(self):
        """Update balance"""
        from db_connection import get_conn
        from queries import UPDATE_PLAYER_BALANCE
        conn = get_conn()
        try:
            cur = conn.cursor()
            
            cur.execute(UPDATE_PLAYER_BALANCE, (self.balance, self.points, self.id))
            conn.commit()
            print(f"BD ACTUALIZADA: {self.name}")
            
        except Exception as e:
            print(f"ERROR en BD: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def get_all_players(cls):
        """Get all players info"""
        from db_connection import get_conn
        from queries import ALL_PLAYERS
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(ALL_PLAYERS)
            rows = cur.fetchall()
            return [cls(row[0], row[1], float(row[2]), float(row[3])) for row in rows]
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        cards_str = " ".join(str(card) for card in self.hand)
        status = "FOLDED" if self.folded else f" Balance: ${self.balance}"
        return f"{self.name} - {cards_str} - {status}"
    
    