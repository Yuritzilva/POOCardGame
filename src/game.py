#Game class
from deck import Deck
class Game:
    def __init__(self, game_id=None, players=None, deck_type="English"):
        self.game_id = game_id  
        self.players = players or []  
        self.deck = None
        self.community_cards = [] 
        self.pot = 0
        self.current_round = 0  
        self.winners = []
        self.is_active = False
        self.deck_type = deck_type
        self.player_actions = []  # Registro de todas las acciones
    
    def start_game(self):
        print("Starting new poker game...")
        
        # 1. Create game in DB
        self._create_game_in_db()
        
        # 2. Create deck and shuffle it
        self.deck = Deck(self.game_id, self.deck_type)
        self.deck.shuffle_cards()
        
        # 3. Reset players
        for player in self.players:
            player.reset_for_new_round()
        
        # 4. Deal cards
        self._deal_private_cards()
        
        # 5. Start first round
        self.current_round = 0 
        self.is_active = True
        
        print(f"Game started! Players: {len(self.players)}, Deck: {self.deck_type}")
    
    def _create_game_in_db(self):
        """Create game in DB"""
        from db_connection import get_conn
        from queries import START_GAME
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(START_GAME)  
            conn.commit()
            self.game_id = cur.lastrowid
            print(f"Game created in DB: ID {self.game_id}")
        except Exception as e:
            print(f"Error creating game in DB: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    
    def _deal_private_cards(self):
        """Deal 2 cards to each player"""
        print("Dealing private cards...")
        for player in self.players:
            card1 = self.deck.deal_card()
            card2 = self.deck.deal_card()
            player.receive_card(card1)
            player.receive_card(card2)
            
            # Save hand in DB
            self._save_player_hand(player)
            
            print(f"   {player.name}: {card1} {card2}")
    
    def _save_player_hand(self, player):
        """Save hand in DB"""
        from db_connection import get_conn
        from queries import INSERT_HAND, INSERT_CARDS_IN_HAND
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(INSERT_HAND, (self.game_id, player.id))
            hand_id = cur.lastrowid
            
            for card in player.hand:
                cur.execute(INSERT_CARDS_IN_HAND ,(hand_id, card.id))
            
            conn.commit()
        except Exception as e:
            print(f" Error saving hand to DB: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    
    def next_round(self):
        """Move between rounds"""
        if not self.is_active:
            return False
        
        round_names = ["Pre-flop", "Flop", "Turn", "River", "Showdown"]
        
        if self.current_round < 4:  # Max round is showdown with 5 cards
            self.current_round += 1
            
            # Deal cards depending on round 
            if self.current_round == 1:  # Flop: 3 cards
                self._deal_community_cards(3)
            elif self.current_round in [2, 3]:  # Turn, River: 1 card
                self._deal_community_cards(1)
            elif self.current_round == 4:  # Showdown: determinate winner
                self._determine_winner()
                self.is_active = False
            
            print(f"Round: {round_names[self.current_round]}")
            return True
        
        return False
    
    def _deal_community_cards(self, count):
        """Deal community hand"""
        for _ in range(count): #Repeat the action 
            card = self.deck.deal_card()
            if card:
                self.community_cards.append(card)
        print(f"Community cards: {[str(c) for c in self.community_cards]}")
    
    def record_player_action(self, player, action, amount=0):
        """Record player action"""
        action_record = {
            'player': player,
            'action': action,  # 'bet', 'fold', 'check', 'raise'
            'amount': amount,
            'round': self.current_round,
        }
        self.player_actions.append(action_record)
        
        # Save in Plays
        self._save_play_to_db(player, action, amount)
        
        print(f"Saved: {player.name} -> {action} \n Bet: ${amount}")
    
    def _save_play_to_db(self, player, action, amount):
        """Save recorded action in DB"""
        from db_connection import get_conn
        from queries import INSERT_PLAY
        conn = get_conn()
        try:
            cur = conn.cursor()
            # using hand_id of current player
            cur.execute(INSERT_PLAY,(self.game_id, player.id, f"{action}:${amount}"))
            conn.commit()
        except Exception as e:
            print(f"Error saving play to DB: {e}")
        finally:
            cur.close()
            conn.close()
    
    def _determine_winner(self):
        """Determine which player/s had won the game"""
        print("Determining winner...")
        
        # Use active players only (not folded)
        active_players = [p for p in self.players if not p.folded]
        
        print(f"   Active players: {[p.name for p in active_players]}")
        print(f"   Folded players: {[p.name for p in self.players if p.folded]}")

        if len(active_players) == 0:
            print("No active players!")
            return
        
        if len(active_players) == 1:
            # unique player
            winner = active_players[0]
            winner.add_winnings(self.pot, 10)  # at least get a high card
            self.winners = [winner]
            self._update_winner_in_db(winner)
            print(f"Winner: {winner.name} - Prize: ${self.pot}")
            return

        #2 or more active players
        # Evaluate each hand
        best_hand_value = -1
        winners = []
        
        for player in active_players:
            from gameRule import GameRule
            hand_evaluation = GameRule.evaluate_hand(player.hand, self.community_cards)
            
            print(f"   {player.name}: {hand_evaluation.name} (Value: {hand_evaluation.value})")
            
            if hand_evaluation.value > best_hand_value:
                best_hand_value = hand_evaluation.value
                winners = [(player, hand_evaluation.value)]
            elif hand_evaluation.value == best_hand_value:
                winners.append((player, hand_evaluation.value))
        
        # Distribute pot and points
        prize_per_winner = self.pot / len(winners)
        for player, hand_value in winners:
            player.add_winnings(prize_per_winner, hand_value)
            self.winners.append(player)
        
        # update winners
        self._update_winner_in_db(winners[0][0])  # Use first winner as reference
        
        print(f"Winners: {[w.name for w in self.winners]} - Prize: ${prize_per_winner} each")
    
    def _update_winner_in_db(self, winner):
        """Update game with winner (player) in DB"""
        from db_connection import get_conn
        from queries import ADD_WINNER
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(ADD_WINNER ,(winner.id, self.game_id))
            conn.commit()
            print(f"Winner updated in DB: {winner.name}")
        except Exception as e:
            print(f"Error updating winner in DB: {e}")
        finally:
            cur.close()
            conn.close()
    
    def get_game_history(self):
        """Get current game history"""
        return {
            'game_id': self.game_id,
            'players': [p.name for p in self.players],
            'community_cards': [str(c) for c in self.community_cards],
            'pot': self.pot,
            'winners': [w.name for w in self.winners],
            'actions': self.player_actions
        }
    
    def __str__(self):
        status = "Active" if self.is_active else "Finished"
        return f"Game {self.game_id} - {status} - Players: {len(self.players)} - Pot: ${self.pot}"