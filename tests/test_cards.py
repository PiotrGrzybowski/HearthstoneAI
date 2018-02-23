import unittest
from functools import partial

from HeartstoneAI.cards import CombatCard, Spell, Hero
import HeartstoneAI.abilities as abilities
from HeartstoneAI.state import Player, State


class TestCards(unittest.TestCase):
    def setUp(self):
        self.ability_1 = {'deal_damage_to_opponent': partial(abilities.deal_damage_to_opposite_player, damage=2)}
        self.ability_2 = {'divine_shield': abilities.do_nothing}

        self.card_1 = CombatCard(name='C1', cost=1, abilities=dict(), attack=1, health=1)
        self.card_2 = CombatCard(name='C2', cost=1, abilities=dict(), attack=1, health=1)

        self.card_3 = CombatCard(name='C3', cost=1, abilities=dict(), attack=2, health=2)
        self.card_4 = CombatCard(name='C4', cost=1, abilities=dict(), attack=2, health=2)

        self.card_5 = CombatCard(name='C5', cost=1, abilities=dict(), attack=3, health=3)
        self.card_6 = CombatCard(name='C6', cost=1, abilities=dict(), attack=3, health=3)

        self.card_7 = CombatCard(name='C5', cost=1, abilities=dict(), attack=4, health=4)
        self.card_8 = CombatCard(name='C6', cost=1, abilities=dict(), attack=4, health=4)

        self.card_8.abilities['charge'] = partial(abilities.charge, card=self.card_8)

        self.spell_1 = Spell(name='PaSpell', cost=1, abilities={**self.ability_1, **self.ability_2})

        self.hero_1 = Hero(name='Pamisio', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)
        self.hero_2 = Hero(name='Pamewcia', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)

        self.first_player = Player(self.hero_1, [], [], [], [])
        self.second_player = Player(self.hero_2, [], [], [], [])

        self.state = State(self.first_player, self.second_player)

    def test_play_spell(self):
        self.first_player.hand = [self.card_1, self.spell_1]
        self.first_player.board = [self.card_3]

        self.state.play_card(1)

        self.assertEqual(self.first_player.hand, [self.card_1])
        self.assertEqual(self.first_player.board, [self.card_3])
        self.assertEqual(self.first_player.graveyard, [self.spell_1])
        self.assertEqual(self.second_player.hero.health, 18)

    def test_attack_minion_by_minion_1(self):
        self.first_player.board = [self.card_1, self.card_3]
        self.second_player.board = [self.card_2, self.card_4]

        self.state.attack(0, 1)
        self.assertEqual(self.first_player.graveyard, [self.card_1])
        self.assertEqual(self.first_player.board, [self.card_3])
        self.assertEqual(self.second_player.board, [self.card_2, self.card_4])
        self.assertEqual(self.second_player.board[1].health, 1)

    def test_attack_minion_by_minion_2(self):
        self.first_player.board = [self.card_1, self.card_3]
        self.second_player.board = [self.card_2, self.card_4]

        self.state.attack(1, 0)
        self.assertEqual(self.first_player.board, [self.card_1, self.card_3])
        self.assertEqual(self.second_player.board, [self.card_4])
        self.assertEqual(self.second_player.graveyard, [self.card_2])
        self.assertEqual(self.first_player.board[1].health, 1)


if __name__ == '__main__':
    unittest.main()
