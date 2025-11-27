#hand class
from db_connection import get_conn  
class Hand:
    def __init__(self, hand_id=None, player_id=None):
        self.hand_id = hand_id     
        self.player_id = player_id 
        self.cards = []            
        self.hand_type = None      
        self.hand_value = 0         
        self.created_at = None      
    
    def add_card(self, card):
        """Add a private card to hand (max 2)"""
        if len(self.cards) < 2:
            self.cards.append(card)
        else:
            print("Hand already has 2 private cards")
    
    def evaluate_hand(self, community_cards):
        """Evaluate hand using private cards + community cards"""
        if len(self.cards) != 2:
            print("Need 2 private cards to evaluate")
            return None
        
        #Can start evaluating game from 3-5 cards in the community_cards
        if len(community_cards) < 3 or len(community_cards) > 5:
            print("Need 3-5 community cards to evaluate")
            return None
        
        # Combine all cards
        all_cards = self.cards + community_cards
        
        # Evaluate hands depending of game phases
        if len(community_cards) == 3:
            self.hand_type = "Post-Flop Evaluation"
            #probability
        elif len(community_cards) == 4:
            self.hand_type = "Post-Turn Evaluation"
            #probability  
        else:  
            self.hand_type = "Final Hand Evaluation"
            #real value
        
        self.hand_value = len(community_cards) * 10  
        return self.hand_type
    
    def save_to_db(self, game_id):
        """Save hand to database"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            
            cur.execute(
                "INSERT INTO Hand (game_id, player_id) VALUES (%s, %s)",
                (game_id, self.player_id)
            )
            self.hand_id = cur.lastrowid
            
            for card in self.cards:
                cur.execute(
                    "INSERT INTO PlayerHandCards (hand_id, card_id) VALUES (%s, %s)",
                    (self.hand_id, card.id)
                )
            
            conn.commit()
            print(f"Hand saved to DB (ID: {self.hand_id})")
            
        except Exception as e:
            print(f"Error saving hand to DB: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    
    def reset_hand(self):
        """Clear hand for new round"""
        self.cards = []
        self.hand_type = None
        self.hand_value = 0
    
    def __str__(self):
        cards_str = " ".join(str(card) for card in self.cards)
        return f"Hand {self.hand_id}: {cards_str} ({self.hand_type})"