class Player:
    def __init__(self, hero, hand, deck, graveyard, board):
        self.hero = hero
        self.hand = hand
        self.deck = deck
        self.graveyard = graveyard
        self.board = board


class State:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
