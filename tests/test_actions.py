import numpy as np
import unittest
import json
from deepdiff import DeepDiff

from copy import deepcopy

from HearthstoneAI import action_tree
from HearthstoneAI import evaluation_utils
from HearthstoneAI.action_tree import walk, get_leafs, get_new_state
from HearthstoneAI.actions_generation import get_cards_play_combinations, get_cards_to_play
from HearthstoneAI.cards import Hero
from HearthstoneAI.cards_generator import card_from_json
from HearthstoneAI.mcts import perform_mcts
from HearthstoneAI.state import Player, State
from settings import CARDS_FILE


class TestActions(unittest.TestCase):
    def setUp(self):
        with open(CARDS_FILE) as json_file:
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

    def test_how_many_combinations_of_playing_cards(self):
        self.state.current_player.hand = [self.abusive_sergeant, self.agent_squire, self.divine_strength,
                                          self.divine_favor]

        player_hand = self.state.current_player.hand
        indexes = np.arange(len(player_hand))

        self.assertEqual(len(list(get_cards_play_combinations(player_hand, indexes, 0))), 1)
        self.assertEqual(len(list(get_cards_play_combinations(player_hand, indexes, 1))), 4)
        self.assertEqual(len(list(get_cards_play_combinations(player_hand, indexes, 2))), 7)
        self.assertEqual(len(list(get_cards_play_combinations(player_hand, indexes, 3))), 9)

    def test_cards_to_play_with_combination(self):
        self.state.current_player.hand = [self.abusive_sergeant, self.agent_squire, self.selfless_hero]
        self.state.play_cards([self.state.current_player.hand[i] for i in [0, 2]])
        self.assertAlmostEqual(self.state.current_player.board, [self.abusive_sergeant, self.selfless_hero])

    def test_cards_to_play(self):
        self.state.current_player.hand = [self.abusive_sergeant, self.agent_squire, self.selfless_hero]

        combinations = list(get_cards_to_play(self.state.current_player.hand, 1))
        self.assertEqual(combinations[0], [])
        self.assertEqual(combinations[1], [self.abusive_sergeant])
        self.assertEqual(combinations[2], [self.agent_squire])
        self.assertEqual(combinations[3], [self.selfless_hero])

        self.state.play_cards([self.abusive_sergeant])

        self.assertEqual(self.state.current_player.hand, [self.agent_squire, self.selfless_hero])
        self.assertEqual(self.state.current_player.board, [self.abusive_sergeant])

    def test_ewcia(self):
        self.state.current_player.hand = [self.abusive_sergeant, self.agent_squire, self.selfless_hero]
        self.state.current_player.board = [deepcopy(self.abusive_sergeant), deepcopy(self.selfless_hero)]
        for card in self.state.current_player.board:
            card.summoning_sickness = False
        self.state.opposite_player.board = [deepcopy(self.selfless_hero), deepcopy(self.abusive_sergeant)]
        self.state = get_new_state(self.state, 3, evaluation_utils.random_strategy)
        print(str(self.state.opposite_player.hero.health))
        self.state.switch_players()
        print(str(self.state.current_player.hero.health))
        print(str(self.state.opposite_player.hero.health))

    def test_random_moves(self):
        self.state.current_player.hand = [self.abusive_sergeant, self.agent_squire,
                                          self.selfless_hero, self.divine_strength]
        self.state.current_player.board = [deepcopy(self.abusive_sergeant), deepcopy(self.selfless_hero),
                                           deepcopy(self.steward_of_darshire)]
        for card in self.state.current_player.board:
            card.summoning_sickness = False
        self.state.opposite_player.hand = [deepcopy(self.abusive_sergeant), deepcopy(self.agent_squire),
                                            deepcopy(self.selfless_hero), deepcopy(self.divine_strength)]
        self.state.opposite_player.board = [deepcopy(self.abusive_sergeant), deepcopy(self.selfless_hero),
                                           deepcopy(self.steward_of_darshire)]
        # new_state, path = action_tree.walk_random(self.state, 0, 3)
        # print(path)

        perform_mcts({'wins': 0, 'losses': 0, 'state': self.state,
                      'children': [], 'path': '', 'new_turn': True, 'parent': None})
