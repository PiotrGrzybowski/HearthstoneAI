import unittest
import json

from HearthstoneAI.cards import Hero
from HearthstoneAI.cards_generator import card_from_json
from HearthstoneAI.state import Player, State


class TestDeck(unittest.TestCase):
    def setUp(self):
        with open('../HearthstoneAI/cards.json') as json_file:
            data = json.load(json_file)
            self.abusive_sergeant = card_from_json(data[0])
            self.agent_squire = card_from_json(data[1])
            self.divine_strength = card_from_json(data[2])
            self.selfless_hero = card_from_json(data[3])
            self.divine_favor = card_from_json(data[4])
            self.seal_of_champions = card_from_json(data[5])
            self.steward_of_darshire = card_from_json(data[6])
            self.wolfrider = card_from_json(data[7])
            self.blessing_of_kings = card_from_json(data[8])
            self.defender_of_argus = card_from_json(data[9])
        
        self.hero_1 = Hero(name='Pamisio', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)
        self.hero_2 = Hero(name='Pamewcia', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)

        self.first_player = Player(self.hero_1, [], [], [], [])
        self.second_player = Player(self.hero_2, [], [], [], [])

        self.state = State(self.first_player, self.second_player)

    def test_abusive_sergeant(self):
        """
        Give a minion +2_Attack this turn.
        :return:
        """
        self.assertEqual(self.abusive_sergeant.attack, 1)
        self.assertEqual(self.abusive_sergeant.health, 1)
        self.assertEqual(self.abusive_sergeant.cost, 1)

        self.first_player.hand = [self.abusive_sergeant]
        self.first_player.board = [self.agent_squire]

        self.state.play_card(0)
        self.assertEqual(self.state.current_player.hand, [])
        self.assertEqual(self.state.current_player.board, [self.agent_squire, self.abusive_sergeant])
        self.assertEqual(self.agent_squire.attack, 3)

        self.state.compensate_abilities()
        self.assertEqual(self.agent_squire.attack, 1)
        self.state.compensate_abilities()
        self.assertEqual(self.agent_squire.attack, 1)

    def test_agent_squire(self):
        """
        Divine Shield
        :return:
        """
        self.abusive_sergeant.health = 5

        self.assertEqual(self.agent_squire.attack, 1)
        self.assertEqual(self.agent_squire.health, 1)
        self.assertEqual(self.agent_squire.cost, 1)

        self.first_player.board = [self.abusive_sergeant]
        self.second_player.board = [self.agent_squire]

        self.state.attack(0, 0)
        self.assertEqual(self.abusive_sergeant.health, 4)
        self.assertEqual(self.agent_squire.health, 1)

        self.state.disable_sickness()
        self.state.attack(0, 0)
        self.assertEqual(self.abusive_sergeant.health, 3)
        self.assertEqual(self.agent_squire.health, 0)
        self.assertEqual(self.state.opposite_player.graveyard, [self.agent_squire])

    def test_divine_strength(self):
        """
        Give a minion +1/+2.
        :return:
        """
        self.first_player.hand = [self.divine_strength]
        self.first_player.board = [self.abusive_sergeant]
        self.state.play_card(0)

        self.assertEqual(self.abusive_sergeant.attack, 2)
        self.assertEqual(self.abusive_sergeant.health, 3)
        self.assertEqual(self.abusive_sergeant.cost, 1)
        self.assertEqual(self.state.current_player.graveyard, [self.divine_strength])
        self.state.compensate_abilities()
        self.assertEqual(self.abusive_sergeant.attack, 2)
        self.assertEqual(self.abusive_sergeant.health, 3)

    def test_selfless_hero(self):
        """
        Deathrattle: Give a random friendly minion Divine Shield.
        :return:
        """
        self.first_player.board = [self.abusive_sergeant]
        self.second_player.board = [self.selfless_hero]
        self.state.attack(0, 0)

        #TODO Fails because there is no minion that can receive a divine shield. Except to pass.

    def test_divine_favor(self):
        """
        Draw cards until you have as many in hand as your opponent.
        :return:
        """
        self.first_player.hand = [self.divine_favor]
        self.first_player.deck = [self.divine_strength, self.seal_of_champions]
        self.second_player.hand = [self.abusive_sergeant, self.agent_squire]

        self.state.play_card(0)
        self.assertEqual(len(self.first_player.hand), len(self.second_player.hand))
        self.assertEqual(self.first_player.graveyard, [self.divine_favor])

    def test_seal_of_champions(self):
        """
        Give a minion +3 Attack and Divine Shield.
        :return:
        """
        self.selfless_hero.health = 10

        self.first_player.hand = [self.seal_of_champions]
        self.first_player.board = [self.abusive_sergeant]
        self.second_player.board = [self.selfless_hero]

        self.state.play_card(0)
        self.assertEqual(self.abusive_sergeant.attack, 4)
        self.state.switch_players()

        self.state.attack(0, 0)
        self.assertEqual(self.abusive_sergeant.health, 1)
        self.assertEqual(self.selfless_hero.health, 6)
        self.state.disable_sickness()

        self.state.attack(0, 0)
        self.assertLessEqual(self.abusive_sergeant.health, 0)
        self.assertEqual(self.selfless_hero.health, 2)
        self.assertEqual(self.first_player.graveyard, [self.seal_of_champions, self.abusive_sergeant])

    def test_steward_of_darshire(self):
        """
        Divine Shield
        :return:
        """
        self.abusive_sergeant.health = 9
        self.abusive_sergeant.attack = 3

        self.first_player.board = [self.abusive_sergeant]
        self.second_player.board = [self.steward_of_darshire]

        self.state.attack(0, 0)
        self.assertEqual(self.abusive_sergeant.health, 6)
        self.assertEqual(self.steward_of_darshire.health, 3)

        self.state.disable_sickness()
        self.state.attack(0, 0)
        self.assertEqual(self.abusive_sergeant.health, 3)
        self.assertEqual(self.steward_of_darshire.health, 0)
        self.assertEqual(self.state.opposite_player.graveyard, [self.steward_of_darshire])

    def test_wolfrider(self):
        """
        Charge.
        :return:
        """
        self.first_player.hand = [self.wolfrider]
        self.state.play_card(0)
        self.assertEqual(self.wolfrider.summoning_sickness, False)

    def test_blessing_of_kings(self):
        """
        Give a minion +4/+4.
        :return:
        """
        self.first_player.hand = [self.blessing_of_kings]
        self.first_player.board = [self.abusive_sergeant]
        self.state.play_card(0)

        self.assertEqual(self.abusive_sergeant.attack, 5)
        self.assertEqual(self.abusive_sergeant.health, 5)
        self.assertEqual(self.abusive_sergeant.cost, 1)
        self.state.compensate_abilities()
        self.assertEqual(self.abusive_sergeant.attack, 5)
        self.assertEqual(self.abusive_sergeant.health, 5)

    def test_defender_of_argus(self):
        """
        Give your two random minions +1/+1 and Taunt.
        :return:
        """
        self.first_player.hand = [self.defender_of_argus]
        self.first_player.board = [self.abusive_sergeant]
        self.state.play_card(0)

        self.assertEqual(self.abusive_sergeant.attack, 2)
        self.assertEqual(self.abusive_sergeant.health, 2)
        self.assertEqual(self.abusive_sergeant.cost, 1)
        self.assertEqual(self.abusive_sergeant.attack, 2)
        self.assertEqual(self.abusive_sergeant.health, 2)


if __name__ == '__main__':
    unittest.main()
