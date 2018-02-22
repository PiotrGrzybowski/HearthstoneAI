from HeartstoneAI.cards import Minion


class Player:
    def __init__(self, hero, hand, deck, board, graveyard):
        self.hero = hero
        self.hand = hand
        self.deck = deck
        self.board = board
        self.graveyard = graveyard

    def put_down_card(self, card):
        if isinstance(card, Minion):
            self.board.append(card)
        else:
            self.graveyard.append(card)

    def check_card(self, index=None):
        if self.board[index].health <= 0:
            self.graveyard.append(self.board.pop(index))


class State:
    def __init__(self, current_player, opposite_player):
        self.current_player = current_player
        self.opposite_player = opposite_player

    def play_card(self, index):
        card = self.current_player.hand.pop(index)
        for ability in card.abilities:
            ability(self)
        self.current_player.put_down_card(card)

    @staticmethod
    def battle(attacking_card, attacked_card):
        attacking_card.health -= attacked_card.attack
        attacked_card.health -= attacking_card.attack

    def attack(self, attacking_index, attacked_index=None):
        attacked_card = self.current_player.hero if attacked_index is None \
            else self.opposite_player.board[attacked_index]
        self.battle(self.current_player.board[attacking_index], attacked_card)
        self.current_player.check_card(attacking_index)
        if attacked_index is not None:
            self.opposite_player.check_card(attacked_index)
