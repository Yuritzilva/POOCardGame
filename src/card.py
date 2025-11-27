#Card class
import paths
from mysql.queries import INSERT_CARD
from db_connection import get_conn
class Card:
    def __init__(self, id_, value, suit):
        self.id = id_
        self.value = value
        self.suit = suit
        
    def __str__(self):
        return f"{self.value}{self.suit}"

    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def set_card(cls, value, suit): 
        """Create a new card in the database"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                INSERT_CARD
            )
            conn.commit()
            card_id = cur.lastrowid
            return cls(card_id, value, suit)  
        finally:
            cur.close()
            conn.close()