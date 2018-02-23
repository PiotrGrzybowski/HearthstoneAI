import random
from functools import partial


def taunt(state):
    # TODO
    pass


def deal_damage_to_opposite_player(state, damage):
    state.opposite_player.hero.health -= damage


def add_shield_to_own_minion(state):
    minion = random.choise(state.current_player)
    minion.abilities['divine_shield'] = do_nothing


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


def do_nothing(state):
    pass
