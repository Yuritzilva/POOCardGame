
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
            print("Deck successfully shuffled")
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
        
        print("Now let's add a third card")
        # Add another card (3 cards in a hand should fail)
        third_card = deck.deal_card()
        hand.add_card(third_card)  # Shows error
        
        # Reset hand
        hand.reset_hand()
        print(f"After reset: {len(hand.cards)} cards")
        
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_gamerule_basic(): 
    print("=== TEST: GameRule Basic ===")
    try:
        from card import Card
        from gameRule import GameRule
            
        # Create test cards
        card1 = Card(1, "A", "Hearts")
        card2 = Card(2, "A", "Spades")   
        card3 = Card(3, "K", "Hearts")
        card4 = Card(4, "Q", "Diamonds")
        card5 = Card(5, "J", "Clubs")
        card6 = Card(6, "10", "Hearts")
        card7 = Card(7, "9", "Spades")
            
        #Detect pair with private hand
        print("\npair detection")
        private_cards = [card1, card3]  
        community_cards = [card2, card4, card5]

        rule_instance = GameRule.evaluate_hand(private_cards, community_cards)
        print(f"   hand detected: {rule_instance.name}")
        print(f"   Value: {rule_instance.value}")
        print(f"   Cards in the combo: {[str(card) for card in rule_instance.combination]}")
            
        # Verify
        assert rule_instance.name == "One Pair", f"Expected One Pair, got {rule_instance.name}"
        assert rule_instance.value == 20, f"Expected 20, got {rule_instance.value}"
        assert len(rule_instance.combination) == 2, f"Expected 2 cards in combination, got {len(rule_instance.combination)}"
        print("Pair detected succesfully")


         # Show rule information
        print("\nShowing rule information")
        flush_info = GameRule.get_GameRule("Flush")
        print(f"Info Flush: {flush_info}")
        
        assert "Five cards of the same suit" in flush_info
        print("Rules info is working just fine")

        print("\n All tests passed")

        print("Showing highest card without errors")
        # Detect highest card
        print("\nDetect highest card")
        private_cards2 = [card2, card4]  
        community_cards2 = [card5, card6, card7]  
            
        rule_instance2 = GameRule.evaluate_hand(private_cards2, community_cards2)
        print(f"   hand detected: {rule_instance2.name}")
        print(f"   Value: {rule_instance2.value}")
        print(f"   Cards in the combo: {[str(card) for card in rule_instance2.combination]}")
            
        
        assert rule_instance2.name == "High Card", f"Expected High Card, got {rule_instance2.name}"
        assert rule_instance2.value == 10, f"Expected 10, got {rule_instance2.value}"
        print("Highest card detected succesfully")
        

        print("Showing an error example in detecting type")
        # Detect highest card
        print("\nDetect highest card")
        private_cards2 = [card3, card4]  
        community_cards2 = [card5, card6, card7]  
            
        rule_instance2 = GameRule.evaluate_hand(private_cards2, community_cards2)
        print(f"   hand detected: {rule_instance2.name}")
        print(f"   Value: {rule_instance2.value}")
        print(f"   Cards in the combo: {[str(card) for card in rule_instance2.combination]}")
            
        
        assert rule_instance2.name == "High Card", f"Expected High Card, got {rule_instance2.name}"
        assert rule_instance2.value == 10, f"Expected 10, got {rule_instance2.value}"
        print("Highest card detected succesfully")
        
            
    except Exception as e:
        print(f"Error in test_gamerule_basic: {e}")
        import traceback
        traceback.print_exc()    
      

def test_gamerule_advanced():
    """Advanced game rule: two pairs, trio , etc"""
    print("=== TEST: GameRule Advanced ===")
    try:
        from card import Card
        from gameRule import GameRule
        
        # Cards
        card1 = Card(1, "A", "Hearts")
        card2 = Card(2, "A", "Spades")
        card3 = Card(3, "K", "Hearts")
        card4 = Card(4, "K", "Diamonds")  
        card5 = Card(5, "Q", "Clubs")
        card6 = Card(6, "J", "Hearts")
        card7 = Card(7, "10", "Spades")
        
        print("\nCase two pairs: ")
        private_cards = [card1, card3]  
        community_cards = [card2, card4, card5, card6, card7]  
        
        rule_instance = GameRule.evaluate_hand(private_cards, community_cards)
        print(f"   Hand detected: {rule_instance.name}")
        print(f"   Value: {rule_instance.value}")
        print(f"   Card combination: {[str(card) for card in rule_instance.combination]}")
        
        # Shuld detect two pair
        if rule_instance.name == "Two Pair":
            print("  Two pair detected correctly")
            assert len(rule_instance.combination) == 4, "Two Pair should have 4 cards in combination"
        else:
            print(f"   expected Two pairs but got: {rule_instance.name}")
        
    except Exception as e:
        print(f"Error en test_gamerule_advanced: {e}")
        import traceback
        traceback.print_exc()
    print()

def test_all_combinations():
    """test all"""
    print("=== TEST: All Poker Combinations ===")
    
    from card import Card
    from gameRule import GameRule
    
    test_cases = [
        {
            "name": "Royal Flush",
            "private": [Card(1, "10", "Hearts"), Card(2, "J", "Hearts")],
            "community": [
                Card(3, "Q", "Hearts"), Card(4, "K", "Hearts"), 
                Card(5, "A", "Hearts"), Card(6, "2", "Spades"), Card(7, "7", "Diamonds")
            ],
            "expected": ("Royal Flush", 100)
        },
        {
            "name": "Straight Flush", 
            "private": [Card(1, "8", "Hearts"), Card(2, "9", "Hearts")],
            "community": [
                Card(3, "10", "Hearts"), Card(4, "J", "Hearts"), 
                Card(5, "Q", "Hearts"), Card(6, "2", "Spades"), Card(7, "7", "Diamonds")
            ],
            "expected": ("Straight Flush", 90)
        },
        {
            "name": "Four of a Kind",
            "private": [Card(1, "A", "Hearts"), Card(2, "A", "Spades")],
            "community": [
                Card(3, "A", "Diamonds"), Card(4, "A", "Clubs"), 
                Card(5, "K", "Hearts"), Card(6, "2", "Spades"), Card(7, "7", "Diamonds")
            ],
            "expected": ("Four of a Kind", 80)
        },
        {
            "name": "Flush",
            "private": [Card(1, "2", "Hearts"), Card(2, "7", "Hearts")],
            "community": [
                Card(3, "9", "Hearts"), Card(4, "J", "Hearts"), 
                Card(5, "K", "Hearts"), Card(6, "2", "Spades"), Card(7, "7", "Diamonds")
            ],
            "expected": ("Flush", 60)
        },
        {
            "name": "Straight",
            "private": [Card(1, "8", "Hearts"), Card(2, "9", "Spades")],
            "community": [
                Card(3, "10", "Diamonds"), Card(4, "J", "Clubs"), 
                Card(5, "Q", "Hearts"), Card(6, "2", "Spades"), Card(7, "7", "Diamonds")
            ],
            "expected": ("Straight", 50)
        }
    ]
    
    for test in test_cases:
        print(f"\nTesting {test['name']}")
        rule_instance = GameRule.evaluate_hand(test["private"], test["community"])
        
        print(f"   Expected: {test['expected'][0]} (Value: {test['expected'][1]})")
        print(f"   Obtained: {rule_instance.name} (Value: {rule_instance.value})")
        print(f"   Card combination: {[str(card) for card in rule_instance.combination]}")
        
        if rule_instance.name == test['expected'][0] and rule_instance.value == test['expected'][1]:
            print(f"Test {test['name']} detected")
        else:
            print(f"failed detection {test['name']}")

def test_player_management():
    """Player testing"""
    print("=== TEST: Player Management ===")
    try:
        from player import Player
        from card import Card
        
        # Create player
        player = Player.set_player("YURIIIIIIIII", 1000.00)
        print(f"Created player as test: {player.name} - Balance: ${player.balance}")
        
        # make a bet
        bet_amount = player.place_bet(100)
        print(f"{player.name} made a bet\n Bet amount: ${bet_amount} - Current balance: ${player.balance}")
        assert player.balance == 900.00
        assert player.current_bet == 100
        
        # get cards
        card1 = Card(1, "A", "Hearts")
        card2 = Card(2, "K", "Spades")
        player.receive_card(card1)
        player.receive_card(card2)
        print(f"Recieved cards: {player}")
        
        assert len(player.hand) == 2
        assert str(card1) in str(player)
        
        # Fold
        player.fold()
        print(f"{player.name} has folded: {player.folded}")
        assert player.folded == True
        
        # Reset
        player.reset_for_new_round()
        print(f"RESET: {len(player.hand)} cards, folded={player.folded}")
        assert len(player.hand) == 0
        assert player.folded == False
        
        # Add winnings
        player.add_winnings(500, 100)
        print(f"winnings: Balance=${player.balance}, points = {player.points}")
        assert player.balance == 1400.00
        
        print("All test passed")
        
    except Exception as e:
        print(f"Error in test_player_management: {e}")
        import traceback
        traceback.print_exc()
    
def test_complete_game():
    """Simulate a poker game"""
    print("=== TEST: Complete Poker Game ===")
    try:
        from player import Player
        from game import Game
        
        # Create player
        player1 = Player.set_player("Yupo", 1000)
        player2 = Player.set_player("Ivanana", 1000)
        player3 = Player.set_player("Pondo", 1000)
        
        players = [player1, player2, player3]
        
        # Create and start game
        game = Game(players=players)
        game.start_game()
        
        # Simulate rounds
        print("\nSimulating betting round...")
        game.record_player_action(player1, "bet", 50)
        game.record_player_action(player2, "call", 50)
        game.record_player_action(player3, "fold", 0)
        game.pot = 100  # Simulate pot 
        
        # Next round
        for round_num in range(4):
            print(f"\nRound {round_num + 1}")
            if game.next_round():
                print(f"   Community cards: {[str(c) for c in game.community_cards]}")
            else:
                print("   Game finished!")
        
        # Show results
        history = game.get_game_history()
        print(f"Game History:")
        print(f"   Winners: {history['winners']}")
        print(f"   Final Pot: ${history['pot']}")
        
        print("Complete game simulation successful")
        
    except Exception as e:
        print(f"Error in complete game test: {e}")
        import traceback
        traceback.print_exc()
    print()

def run_tests():
    """Ejecute tests"""
    print("Executing...\n")
    
    #test_card_creation()
    #insert_english_deck()
    #test_deck_initialization() 
    #test_deck_shuffling()
    #test_card_dealing()
    #test_hand_management()
    #test_gamerule_basic()
    #test_gamerule_advanced()
    #test_all_combinations()
    #test_player_management()
    test_complete_game()

    print("Test completed")

if __name__ == "__main__":
    run_tests()