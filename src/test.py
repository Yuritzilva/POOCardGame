
"""
Individual testing
"""

from db_connection import get_conn
from card import Card
from deck import Deck
from hand import Hand

def test_card_creation():
    """We want this code to test the creation of the cards"""
    print("=== TEST: Card creation ===")
    card = Card(1, "A", "Hearts")
    print(f"Card created: {card}")
    print(f"   ID: {card.id}, Value: {card.value}, Suit: {card.suit}")
    print()

def insert_english_deck():
    """I want to insert all cards in the database using an english deck"""
    print("=== TEST: Insert multiple cards in database ===")
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    created_cards = []
    
    for suit in suits:
        for value in values:
            try:
                card = Card.set_card(value, suit)
                created_cards.append(card)
                print(f"Created: {card}")
            except Exception as e:
                print(f"Error creating {value} of {suit}: {e}")
    
    return created_cards


def test_deck_initialization():
    """Want to test if the deck initializes correctly"""
    print("=== TEST: Deck Initialization ===")
    try:
        deck = Deck(1, "English")
        print(f"Deck created: {deck.deck_type}")
        print(f" Total cards: {deck.total_cards}")
        print(f" Undealt cards: {len(deck.undealt_cards)}")
        print(f" Is shuffled: {deck.is_shuffled}")
        
        # show cards
        if deck.undealt_cards:
            print(f"   Sample cards: {[str(card) for card in deck.undealt_cards[:3]]}")
        
    except Exception as e:
        print(f"Error while creating deck: {e}")
    print()

def test_deck_shuffling():
    """Shuffle the cards"""
    print("=== TEST: Deck Shuffling ===")
    try:
        deck = Deck(1, "English")
        original_order = [str(card) for card in deck.undealt_cards[:5]]
        
        print("Before shuffle:", original_order)
        deck.shuffle_cards()
        
        new_order = [str(card) for card in deck.undealt_cards[:5]]
        print("After shuffle: ", new_order)
        
        # Check if order is not the same as the original order
        if original_order != new_order:
            print("✅ Deck successfully shuffled")
        else:
            print("Deck order may not have changed")
            
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_card_dealing():
    """Deal cards"""
    print("=== TEST: Card Dealing ===")
    try:
        deck = Deck(1, "English")
        initial_count = len(deck.undealt_cards)
        
        deck.shuffle_cards()
        
        # Deal 5 cards
        dealt_cards = []
        for i in range(5):
            card = deck.deal_card()
            if card:
                dealt_cards.append(card)
                print(f"   Dealt {i+1}: {card}")
        
        print(f"    Dealt {len(dealt_cards)} cards")
        print(f"   Remaining in deck: {len(deck.undealt_cards)}")
        print(f"   Dealt counter: {deck.dealt_cards}")
        
        # Verificar contadores
        if deck.dealt_cards == len(dealt_cards):
            print("Deal counter correct")
        else:
            print("Deal counter mismatch")
            
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_hand_management():
    """Create and manage hands"""
    print("=== TEST: Hand Management ===")
    try:
        # Create hand
        hand = Hand(player_id=1)
        print("Hand created")
        
        # Create deck, shuffle deck and deal cards
        deck = Deck(1, "English")
        deck.shuffle_cards()
        
        hand.add_card(deck.deal_card())
        hand.add_card(deck.deal_card())
        
        print(f"Hand has {len(hand.cards)} cards: {hand}")
        
        # Add another card (3 cards in a hand should fail)
        third_card = deck.deal_card()
        hand.add_card(third_card)  # Shows error
        
        # Reset hand
        hand.reset_hand()
        print(f"After reset: {len(hand.cards)} cards")
        
    except Exception as e:
        print(f"Error: {e}")
    print()

def run_tests():
    """Ejecute tests"""
    print("Executing...\n")
    
    #test_card_creation()
    insert_english_deck()
    #test_deck_initialization() 
    #test_deck_shuffling()
    #test_card_dealing()
    #test_hand_management()
    
    print("Test completed")

if __name__ == "__main__":
    run_tests()