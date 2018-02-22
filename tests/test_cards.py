import unittest
from functools import partial

from HeartstoneAI.cards import CombatCard, Spell, Hero
from HeartstoneAI.flow import deals_manage_to_opposite_player
from HeartstoneAI.state import Player, State

ABILITY_1 = partial(deals_manage_to_opposite_player, damage=2)

CARD_1 = CombatCard(name='Ewcia', cost=1, abilities=[], attack=1, health=2)
CARD_2 = CombatCard(name='Misio', cost=1, abilities=[], attack=1, health=2)
CARD_3 = CombatCard(name='Pamewcia', cost=1, abilities=[], attack=1, health=2)
CARD_4 = CombatCard(name='Pamisio', cost=1, abilities=[], attack=1, health=2)
SPELL_1 = Spell(name='PaSpell', cost=1, abilities=[ABILITY_1])

HERO_1 = Hero(name='Pamisio', cost=0, abilities=[], attack=0, health=20, hero_class=None)
HERO_2 = Hero(name='Pamewcia', cost=0, abilities=[], attack=0, health=20, hero_class=None)


class TestCards(unittest.TestCase):
    def test_play_spell(self):
        first_player = Player(hero=HERO_1, hand=[CARD_1, SPELL_1], deck=[CARD_2], board=[CARD_3], graveyard=[])
        second_player = Player(hero=HERO_2, hand=[], deck=[], board=[], graveyard=[])
        state = State(first_player, second_player)

        state.play_card(1)

        self.assertEqual(first_player.hand, [CARD_1])
        self.assertEqual(first_player.board, [CARD_3])
        self.assertEqual(first_player.graveyard, [SPELL_1])
        self.assertEqual(second_player.hero.health, 18)


if __name__ == '__main__':
    unittest.main()
