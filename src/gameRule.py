class GameRule:    
    def __init__(self, id_=None, name=None, value=None, combination = None):
        self.id = id_
        self.name = name  
        self.value = value  
        self.combination = [] or combination # Cards making the specific game rule
    
    # Dictionary of poker game rules :)
    HAND_RULES = {
        "Royal Flush": {
            "value": 100,
            "description": "10, J, Q, K, A same suit"
        },
        "Straight Flush": {
            "value": 90,
            "description": "Five cards in a numeric sequence same suit"
        },
        "Four of a Kind": {
            "value": 80,
            "description": "Four cards of the same value"
        },
        "Full House": {
            "value": 70, 
            "description": "A trio and a pair"
        },
        "Flush": {
            "value": 60,
            "description": "Five cards of the same suit"
        },
        "Straight": {
            "value": 50,
            "description": "Five cards in a numeric sequence"
        },
        "Three of a Kind": {
            "value": 40,
            "description": "Three cards of the same value"
        },
        "Two Pair": {
            "value": 30,
            "description": "Two pair of cards of the same value"
        },
        "One Pair": {
            "value": 20,
            "description": "Two cards of the same value"
        },
        "High Card": {
            "value": 10,
            "description": "Highest value card in your hand"
        }
    }
    
    @classmethod
    def set_GameRule(cls, name, value, description):
        """Crete new game rule: i will not be able to develop this part
        where you can build your own game :( 
        """
        cls.HAND_RULES[name] = {
            "value": value,
            "description": description
        }
        return f"Rule {name} created"
    
    @classmethod
    def get_GameRule(cls, rule_name):
        """Obtain information about a specific rule"""
        rule = cls.HAND_RULES.get(rule_name)
        if rule:
            return f"{rule_name}: {rule['description']} (value: {rule['value']})"
        return "Rule not found"
    
    @classmethod
    def evaluate_hand(cls, private_cards, community_cards):
        """Evaluate hand and show best combo posible"""
        all_cards = private_cards + community_cards
        
        # evaluate, first best hand to worse
        royal_flush = cls._check_royal_flush(all_cards)
        if royal_flush:
            return cls(None, "Royal Flush", 100, royal_flush)
        
        straight_flush = cls._check_straight_flush(all_cards)
        if straight_flush:
            return cls(None, "Straight Flush", 90, straight_flush)
        
        four_of_a_kind = cls._check_four_of_a_kind(all_cards)
        if four_of_a_kind:
            return cls(None, "Four of a Kind", 80, four_of_a_kind)
        
        full_house = cls._check_full_house(all_cards)
        if full_house:
            return cls(None, "Full House", 70, full_house)
        
        flush = cls._check_flush(all_cards)
        if flush:
            return cls(None, "Flush", 60, flush)
        
        straight = cls._check_straight(all_cards)
        if straight:
            return cls(None, "Straight", 50, straight)
        
        # if there is no complex hand then use a simple evaluation
        hand_name, hand_value, combination_cards = cls._simple_evaluation(all_cards)
        return cls(None, hand_name, hand_value, combination_cards)
    
    @classmethod
    def _simple_evaluation(cls, cards):
        """simple evaluation - returns (name, value, card combination)"""
        from collections import Counter
        
        values = [card.value for card in cards]
        value_counts = Counter(values)
        
        # Detect pairs or trios and get the specific cards
        pairs = []
        trios = []
        
        for value, count in value_counts.items():
            if count == 2:
                # find the cards that make the pairs
                pair_cards = [card for card in cards if card.value == value]
                pairs.append(pair_cards)
            elif count == 3:
                # find the cards that make the trio
                trio_cards = [card for card in cards if card.value == value]
                trios.append(trio_cards)
        
        # Determinate best hand
        if trios and pairs:
            # Full House: trio + pair
            combination = trios[0] + pairs[0][:2]  # Take only 2 cards from pair
            return "Full House", 70, combination
        elif trios:
            return "Three of a Kind", 40, trios[0]
        elif len(pairs) >= 2:
            # Two Pair: two different pairs
            combination = pairs[0] + pairs[1]
            return "Two Pair", 30, combination
        elif len(pairs) == 1:
            #One pair
            return "One Pair", 20, pairs[0]
        else:
            # High Card: The highest card
            high_card = max(cards, key=lambda card: cls._card_value_to_int(card.value))
            return "High Card", 10, [high_card]
    
    @classmethod
    def _card_value_to_int(cls, value):
        """Conver card value to compare"""
        value_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                    '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return value_map.get(value, 0)
    
    @classmethod
    def _check_royal_flush(cls, cards):
        """Verify Royal Flush 10,J,Q,K,A same suit"""
        straight_flush = cls._check_straight_flush(cards)
        if straight_flush:
            # Verify using a straight flush
            values = {card.value for card in straight_flush}
            if {'10', 'J', 'Q', 'K', 'A'} == values:
                return straight_flush
        return None

    @classmethod
    def _check_straight_flush(cls, cards):
        """Verify a straight flush 5 consecutive cards"""
        # group by suit
        suits = {}
        for card in cards:
            if card.suit not in suits:
                suits[card.suit] = []
            suits[card.suit].append(card)
        
        # for each suit find a flush
        for suit, suit_cards in suits.items():
            if len(suit_cards) >= 5:
                straight = cls._find_straight(suit_cards)
                if straight:
                    return straight
        return None

    @classmethod
    def _check_four_of_a_kind(cls, cards):
        """Verify four of a kind, four cards same suit"""
        from collections import Counter
        values = [card.value for card in cards]
        value_counts = Counter(values)
        
        for value, count in value_counts.items():
            if count >= 4:
                four_cards = [card for card in cards if card.value == value]
                return four_cards[:4]
        return None

    @classmethod
    def _check_full_house(cls, cards):
        """Verify Full House - trio + pair"""
        from collections import Counter
        values = [card.value for card in cards]
        value_counts = Counter(values)
        
        # Search trio and pair
        trio_value = None
        pair_value = None
        
        for value, count in value_counts.items():
            if count >= 3 and not trio_value:
                trio_value = value
            elif count >= 2 and value != trio_value and not pair_value:
                pair_value = value
        
        if trio_value and pair_value:
            trio_cards = [card for card in cards if card.value == trio_value][:3]
            pair_cards = [card for card in cards if card.value == pair_value][:2]
            return trio_cards + pair_cards
        
        return None

    @classmethod
    def _check_flush(cls, cards):
        """Verify Flush 5 cards same suit"""
        suits = {}
        for card in cards:
            if card.suit not in suits:
                suits[card.suit] = []
            suits[card.suit].append(card)
        
        for suit, suit_cards in suits.items():
            if len(suit_cards) >= 5:
                # order and take first 5
                sorted_cards = sorted(suit_cards, key=lambda x: cls._card_value_to_int(x.value), reverse=True)
                return sorted_cards[:5]
        return None

    @classmethod
    def _check_straight(cls, cards):
        """verify straight"""
        return cls._find_straight(cards)

    @classmethod
    def _find_straight(cls, cards):
        """find 5 consecutive cards without specific suit"""
        # Convert values to number and delete duplicates
        unique_values = set()
        for card in cards:
            unique_values.add(cls._card_value_to_int(card.value))
        
        # look for consecutive cards
        sorted_values = sorted(unique_values, reverse=True)
        
        for i in range(len(sorted_values) - 4):
            if sorted_values[i] - sorted_values[i+4] == 4:
                # find specific cards 
                straight_values = set(range(sorted_values[i+4], sorted_values[i] + 1))
                straight_cards = []
                for value in sorted_values[i:i+5]:
                    # find a card for value
                    for card in cards:
                        if cls._card_value_to_int(card.value) == value and card not in straight_cards:
                            straight_cards.append(card)
                            break
                return straight_cards[:5]
        
        # Special consecutive is A (14),2,3,4,5
        if {14, 2, 3, 4, 5}.issubset(unique_values):
            straight_cards = []
            for value in [5, 4, 3, 2, 14]:  
                for card in cards:
                    if cls._card_value_to_int(card.value) == value and card not in straight_cards:
                        straight_cards.append(card)
                        break
            return straight_cards
        
        return None 
    
    def __str__(self):
        cards_str = " ".join(str(card) for card in self.combination)
        return f"{self.name} (Value: {self.value}) - Cards: {cards_str}"

    