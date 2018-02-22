class Player:
    def __init__(self, hero, hand, deck, graveyard, board):
        self.hero = hero
        self.hand = hand
        self.deck = deck
        self.graveyard = graveyard
        self.board = board


class State:
    def __init__(self, current_player, opposite_player):
        self.current_player = current_player
        self.opposite_player = opposite_player


class Game:
    def __init__(self, state):
        self.state = state

    def play_card(self, card):
        for ability in card.abilities:
            ability(self.state)

