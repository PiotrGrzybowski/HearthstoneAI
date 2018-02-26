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
    if state.current_player.board:
        minion = random.choice(state.current_player.board)
        minion.abilities[DIVINE_SHIELD] = divine_shield


def add_ability_and_specs_to_own_minion(state, ability, attack=0, health=0):
    if state.current_player.board:
        minion = random.choice(state.current_player.board)
        minion.abilities = {**minion.abilities, **ability}
        add_specs(attack, health, minion)


def add_divine_shield_and_specs_to_own_minion(state, attack=0, health=0):
    if state.current_player.board:
        minion = random.choice(state.current_player.board)
        minion.abilities[DIVINE_SHIELD] = divine_shield
        add_specs(attack, health, minion)


def add_taunt_and_specs_to_own_minion(state, attack=0, health=0):
    if state.current_player.board:
        minion = random.choice(state.current_player.board)
        minion.abilities[TAUNT] = taunt
        add_specs(attack, health, minion)


def add_specs_to_own_minion_for_turn(state, attack=0, health=0):
    if state.current_player.board:
        minion = random.choice(state.current_player.board)
        add_specs(attack, health, minion)
        state.compensation_abilities['remove_attack'] = partial(add_specs_to_specified_minion, attack=-attack, health=0,
                                                                minion=minion)


def add_specs(attack, health, minion):
    minion.attack += attack
    minion.health += health


def add_specs_to_own_minion(state, health=0, attack=0):
    if state.current_player.board:
        minion = random.choice(state.current_player.board)
        add_specs(attack, health, minion)


def add_specs_to_specified_minion(state, minion=None, health=0, attack=0):
    add_specs(attack, health, minion)


def give_ability_to_minion(minion, ability):
    minion.abilities = {**minion.abilities, **ability}


def charge(state, minion):
    minion.summoning_sickness = False


def divine_shield(state):
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


def get_divine_shield_ability(**kwargs):
    return partial(divine_shield, kwargs)


ABILITIES = {'add_specs_to_own_minion_for_turn': add_specs_to_own_minion_for_turn,
             'divine_shield': divine_shield,
             'charge': charge,
             'add_specs_to_own_minion': add_specs_to_own_minion,
             'add_shield_to_own_minion': add_shield_to_own_minion,
             'draw_cards_to_match_opponent': draw_cards_to_match_opponent,
             'add_divine_shield_and_specs_to_own_minion': add_divine_shield_and_specs_to_own_minion,
             'add_taunt_and_specs_to_own_minion': add_taunt_and_specs_to_own_minion}
