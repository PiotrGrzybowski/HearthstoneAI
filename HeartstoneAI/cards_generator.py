from functools import partial
from HeartstoneAI.abilities import ABILITIES
from HeartstoneAI.cards import Minion, CARD_TYPES

PARAMETERS = {'Minion': ['name', 'cost', 'attack', 'health', 'minion_type'],
              'Spell': ['name', 'cost']}


def get_constructor(card_type):
    return CARD_TYPES[card_type]


def get_parameters(card):
    return {key: card[key] for key in PARAMETERS[card['type']]}


def build_ability(ability):
    return partial(ABILITIES[ability['function']], **ability['kwargs'])


def get_abilities(card):
    return {ability_config['name']: build_ability(ability_config) for ability_config in card['abilities']}


def card_from_json(card):
    return get_constructor(card['type'])(**get_parameters(card), abilities=get_abilities(card))
