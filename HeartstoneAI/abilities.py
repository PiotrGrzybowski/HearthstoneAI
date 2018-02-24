import random
from functools import partial

DIVINE_SHIELD = 'divine_shield'
CHARGE = 'charge'
DEATHRATTLE = 'deathrattle'
TAUNT = 'taunt'


def taunt(state):
    pass


def deal_damage_to_opposite_player(state, damage):
    state.opposite_player.hero.health -= damage


def add_shield_to_own_minion(state):
    minion = random.choice(state.current_player.board)
    minion.abilities[DIVINE_SHIELD] = apply_divine_shield


def add_ability_and_specs_to_own_minion(state, ability, attack=0, health=0):
    minion = random.choice(state.current_player.board)
    minion.abilities = {**minion.abilities, **ability}
    minion.attack += attack
    minion.health += health


def add_specs_to_own_minion_for_turn(state, attack=0, health=0):
    minion = random.choice(state.current_player.board)
    minion.attack += attack
    minion.health += health
    state.compensation_abilities['remove_attack'] = partial(add_specs_to_own_minion,
                                                            attack=-attack, health=0,
                                                            minion=minion)


def add_specs_to_own_minion(state, health=0, attack=0):
    minion = random.choice(state.current_player.board)
    minion.health += health
    minion.attack += attack


def charge(state, minion):
    minion.summoning_sickness = False


def apply_divine_shield(state):
    pass


def draw_cards_to_match_opponent(state):
    card_diff = len(state.opposite_player.hand) - len(state.current_player.hand)
    for i in range(max(0, card_diff)):
        state.draw_card()


def check_divine_shield(attacked_card, attacking_card):
    if DIVINE_SHIELD in attacked_card.abilities:
        attacked_card.abilities.pop(DIVINE_SHIELD)
    else:
        attacked_card.health -= attacking_card.attack
