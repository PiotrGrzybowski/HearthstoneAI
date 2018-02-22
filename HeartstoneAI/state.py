class Player:
    def __init__(self, hero, hand, deck, board, graveyard):
        self.hero = hero
        self.hand = hand
        self.deck = deck
        self.board = board
        self.graveyard = graveyard


class State:
    def __init__(self, current_player, opposite_player):
        self.current_player = current_player
        self.opposite_player = opposite_player

    def play_card(self, index):
        card = self.current_player.hand.pop(index)
        for ability in card.abilities:
            ability(self)
        self.current_player.graveyard.append(card)
