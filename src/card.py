#Card class

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