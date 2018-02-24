import unittest
from functools import partial

from HeartstoneAI.cards import CombatCard, Spell, Hero, Minion
from HeartstoneAI.abilities import CHARGE, DIVINE_SHIELD
import HeartstoneAI.abilities as abilities
from HeartstoneAI.state import Player, State


class TestCards(unittest.TestCase):
    def setUp(self):
        self.ability_1 = {'deal_damage_to_opponent': partial(abilities.deal_damage_to_opposite_player, damage=2)}
        self.ability_2 = {DIVINE_SHIELD: abilities.divine_shield}
        self.ability_charge = {CHARGE: abilities.charge}

        self.card_1 = Minion(name='C1', cost=1, abilities=dict(), attack=1, health=1, minion_type=None)
        self.card_2 = Minion(name='C2', cost=1, abilities=dict(), attack=1, health=1, minion_type=None)

        self.card_3 = Minion(name='C3', cost=1, abilities=dict(), attack=2, health=2, minion_type=None)
        self.card_4 = Minion(name='C4', cost=1, abilities=dict(), attack=2, health=2, minion_type=None)

        self.card_5 = Minion(name='C5', cost=1, abilities=dict(), attack=3, health=3, minion_type=None)
        self.card_6 = Minion(name='C6', cost=1, abilities=dict(), attack=3, health=3, minion_type=None)

        self.card_7 = Minion(name='C7', cost=1, abilities=dict(), attack=4, health=4, minion_type=None)
        self.card_8 = Minion(name='C8', cost=1, abilities=dict(), attack=4, health=4, minion_type=None)

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

    def test_summoning_sickness_is_true_when_minion_is_played(self):
        self.state.current_player.hand = [self.card_1]
        self.state.play_card(0)

        self.assertTrue(self.card_1.summoning_sickness)

    def test_summoning_sickness_when_minion_with_charge_is_played(self):
        self.card_1.abilities[CHARGE] = partial(abilities.charge, minion=self.card_1)
        self.state.current_player.hand = [self.card_1]
        self.state.play_card(0)
        self.assertFalse(self.card_1.summoning_sickness)

    def test_divine_shield_reduce_damage_to_zero_and_disappear(self):
        self.card_1.abilities[DIVINE_SHIELD] = abilities.divine_shield
        self.state.current_player.board = [self.card_2]
        self.state.opposite_player.board = [self.card_1]

        self.state.attack(0, 0)

        self.assertTrue(DIVINE_SHIELD not in self.card_1.abilities)
        self.assertEqual(self.card_2.health, 0)
        self.assertEqual(self.state.current_player.board, [])
        self.assertEqual(self.state.current_player.graveyard, [self.card_2])


if __name__ == '__main__':
    unittest.main()
