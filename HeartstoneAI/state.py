from HeartstoneAI.abilities import check_divine_shield, CHARGE
from HeartstoneAI.cards import Minion
from HeartstoneAI.abilities import DEATHRATTLE

MAX_HAND_SIZE = 10


class Player:
    def __init__(self, hero, hand, deck, board, graveyard):
        self.hero = hero
        self.hand = hand
        self.deck = deck
        self.board = board
        self.graveyard = graveyard
        self.fatigue = 0

    def put_down_card(self, card):
        if isinstance(card, Minion):
            self.board.append(card)
        else:
            self.graveyard.append(card)

    def validate_card(self, index, state):
        card = self.board[index]
        if card.health <= 0:
            if DEATHRATTLE in card.abilities:
                card.abilities[DEATHRATTLE](state)
            self.graveyard.append(self.board.pop(index))

    def draw_card(self):
        if len(self.hand) < MAX_HAND_SIZE:
            self.hand.append(self.deck.pop())
        else:
            self.graveyard.append(self.deck.pop())

    def apply_fatigue(self, amount=1):
        self.fatigue += amount
        self.hero.health -= self.fatigue

    def disable_sickness(self):
        for minion in self.board:
            minion.summoning_sickness = False

    @property
    def is_dead(self):
        return self.hero.health <= 0


class State:
    def __init__(self, current_player, opposite_player):
        self.current_player = current_player
        self.opposite_player = opposite_player
        self.compensation_abilities = dict()

    def play_card(self, index):
        card = self.current_player.hand.pop(index)
        for name, ability in card.abilities.items():
            if name == CHARGE:
                card.summoning_sickness = False
            elif name != DEATHRATTLE:
                ability(self)
        self.current_player.put_down_card(card)

    @staticmethod
    def battle(attacking_card, attacked_card):
        check_divine_shield(attacked_card, attacking_card)

        attacking_card.health -= attacked_card.attack
        attacking_card.summoning_sickness = True

    def attack(self, attacking_index, attacked_index):
        self.battle(self.current_player.board[attacking_index], self.opposite_player.board[attacked_index])
        self.current_player.validate_card(attacking_index, self)
        self.opposite_player.validate_card(attacked_index, self)

    def attack_hero(self, attacking_index):
        self.battle(self.current_player.board[attacking_index], self.opposite_player.hero)
        self.current_player.validate_card(attacking_index, self)

    def switch_players(self):
        temp_player = self.current_player
        self.current_player = self.opposite_player
        self.opposite_player = temp_player

    def draw_card(self):
        if self.current_player.deck:
            self.current_player.draw_card()
        else:
            self.current_player.apply_fatigue()

    @property
    def is_terminal(self):
        return self.current_player.is_dead or self.opposite_player.is_dead

    def disable_sickness(self):
        self.current_player.disable_sickness()

    def compensate_abilities(self):
        for _, ability in self.compensation_abilities.items():
            ability(self)
        self.compensation_abilities = {}
