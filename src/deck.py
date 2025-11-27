#Deck class
from db_connection import get_conn
from card import Card
import random
class Deck:
    def __init__(self, id_, deck_type = "English"):
        self.id = id_
        self.is_shuffled = False
        self.total_cards = 0
        self.deck_type = deck_type
        self.undealt_cards = []
        self.dealt_cards = 0
        self.load_cards_from_db()

    def load_cards_from_db(self):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cards_per_suit = 0 

            if self.deck_type == "Spanish":
                target_suits = ['Oros', 'Copas', 'Espadas', 'Bastos']
                cards_per_suit = 12
            else:
                #Default deck
                target_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']  
                cards_per_suit = 13
            
            cur.execute("SELECT card_id, card_value, suit FROM Cards")
            all_cards = cur.fetchall()
            
            self.undealt_cards = []

            #Filter out cards that match our deck
            for card_id, card_value, suit in all_cards:
                if suit in target_suits: 
                    # Create object Card and add it to deck
                    card = Card(card_id, card_value, suit)
                    self.undealt_cards.append(card)
            
            #Count cards
            expected_count = cards_per_suit * len(target_suits)  
            if len(self.undealt_cards) != expected_count:
                print(f"Warning! \n Loaded cards: {len(self.undealt_cards)} \n Cards expected: {expected_count}")
                
            print(f"Current deck: ({self.deck_type})\n Total cards: {len(self.undealt_cards)}")
            self.total_cards = len(self.undealt_cards)

        except Exception as e:
            print(f"Card loading error: {e}")
            self.undealt_cards = []  # Asegurar que cards no sea None
        finally:
            cur.close()
            conn.close()
                
    def shuffle_cards(self):
        """Reorganize cards in a random order"""

        if not self.undealt_cards or len(self.undealt_cards) < self.total_cards:
            print("Cards do not exist")
        else:
            random.shuffle(self.undealt_cards)
            self.is_shuffled = True
            print("Shuffled deck")

    def deal_card(self):
        """Take one card and asign it to a hand (current_player_hand)"""
        
        if self.undealt_cards:
            card = self.undealt_cards.pop() 
            print("Dealt card")
            self.dealt_cards += 1
            return card
        
        else: 
            print("No cards to deal")
        return None

    def reset_deck(self):
        """Reset deck to initial state"""
        self.load_cards_from_db() 
        self.is_shuffled = False
        self.dealt_cards = 0
        print("Deck reseted")
