#player class
class Player:
    def __init__(self, id_, name, bet, balance, is_bot=False):
        self.id = id_
        self.name = name
        self.bet = bet
        self.points = 0
        self.balance = balance
        self.folded = False #is playing / folded
        self.is_bot = is_bot
        self.hand = []
        self.current_bet = 0 

    @classmethod
    def get_player():
        pass

    @classmethod
    def set_player():
        pass

    def add_winnings():
        pass
    
    def receive_card(self, card):
        self.hand.append(card)

    def reset_hand(self):
        self.hand = []
        self.current_bet = 0
        self.folded = False
        self.all_in = False

    def __str__(self):
        return f"{self.name} – {self.hand}"