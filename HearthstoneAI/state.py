import numpy as np

from deepdiff import DeepDiff

from HearthstoneAI.abilities import check_divine_shield, CHARGE
from HearthstoneAI.cards import Minion
from HearthstoneAI.abilities import DEATHRATTLE

MAX_HAND_SIZE = 10


class Player:
    def __init__(self, hero, hand, deck, board, graveyard):
        self.hero = hero
        self.hand = hand
        self.deck = deck
        self.board = board
        self.graveyard = graveyard
        self.fatigue = 0
        self.mana = 0

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

    def validate_card_by_ref(self, card, state):
        if card.health <= 0:
            if DEATHRATTLE in card.abilities:
                card.abilities[DEATHRATTLE](state)
            self.graveyard.append(card)
            self.board.remove(card)

    def draw_card(self):
        index = np.random.randint(len(self.deck))
        if len(self.hand) < MAX_HAND_SIZE:
            self.hand.append(self.deck.pop(index))
        else:
            self.graveyard.append(self.deck.pop(index))

    def apply_fatigue(self, amount=1):
        self.fatigue += amount
        self.hero.health -= self.fatigue

    def disable_sickness(self):
        for minion in self.board:
            minion.summoning_sickness = False

    @property
    def is_dead(self):
        return self.hero.health <= 0

    @property
    def health(self):
        return max(0, self.hero.health)

    @property
    def name(self):
        return self.hero.name

    def __hash__(self):
        return hash((tuple(self.board), tuple(self.deck), self.fatigue,
                     tuple(self.graveyard), tuple(self.hand), self.hero))


class State:
    def __init__(self, current_player, opposite_player):
        self.current_player = current_player
        self.opposite_player = opposite_player
        self.compensation_abilities = dict()
        self.mana = 1

    def play_card(self, index):
        card = self.current_player.hand.pop(index)
        self.apply_abilities(card)
        self.current_player.put_down_card(card)

    def play_card_by_ref(self, card):
        self.apply_abilities(card)
        self.current_player.put_down_card(card)
        self.current_player.hand.remove(card)

    def apply_abilities(self, card):
        for name, ability in card.abilities.items():
            if name == CHARGE:
                card.summoning_sickness = False
            elif name != DEATHRATTLE:
                ability(self)

    def play_cards(self, cards):
        for card in cards:
            self.apply_abilities(card)
            self.current_player.put_down_card(card)
            self.current_player.hand.remove(card)

    @staticmethod
    def battle(attacking_card, attacked_card):
        check_divine_shield(attacked_card, attacking_card)
        attacking_card.health -= attacked_card.attack
        attacking_card.summoning_sickness = True

    def attack(self, attacking_index, attacked_index):
        self.battle(self.current_player.board[attacking_index], self.opposite_player.board[attacked_index])
        self.current_player.validate_card(attacking_index, self)
        self.opposite_player.validate_card(attacked_index, self)

    def attack_by_ref(self, attacking_card, attacked_card):
        self.battle(attacking_card, attacked_card)
        self.current_player.validate_card_by_ref(attacking_card, self)
        self.opposite_player.validate_card_by_ref(attacked_card, self)

    def attack_hero(self, attacking_index):
        self.battle(self.current_player.board[attacking_index], self.opposite_player.hero)
        self.current_player.validate_card(attacking_index, self)

    def attack_hero_by_ref(self, attacking_card):
        self.battle(attacking_card, self.opposite_player.hero)
        self.current_player.validate_card_by_ref(attacking_card, self)

    def switch_players(self):
        temp_player = self.current_player
        self.current_player = self.opposite_player
        self.opposite_player = temp_player

    def draw_card(self):
        if self.current_player.deck:
            self.current_player.draw_card()
        else:
            self.current_player.apply_fatigue()

    def new_turn(self):
        self.mana = min(10, self.mana + 1)
        self.switch_players()
        self.draw_card()
        self.switch_players()
        self.draw_card()

    def new_turn_for_one_player(self):
        self.switch_players()
        self.update_mana()
        self.disable_sickness()
        self.draw_card()

    def update_mana(self):
        self.current_player.mana = min(10, self.current_player.mana + 1)

    @property
    def is_terminal(self):
        return self.current_player.is_dead or self.opposite_player.is_dead

    def disable_sickness(self):
        self.current_player.disable_sickness()

    def compensate_abilities(self):
        for _, ability in self.compensation_abilities.items():
            ability(self)
        self.compensation_abilities = {}

    def get_player_by_name(self, name):
        return self.current_player if self.current_player.name == name else self.opposite_player

    def __hash__(self):
        return hash((self.current_player,
                     self.opposite_player))

    def __eq__(self, other):
        return not DeepDiff(self, other)

    def __ne__(self, other):
        return bool(DeepDiff(self, other))
