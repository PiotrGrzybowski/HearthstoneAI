import numpy as np
import unittest
import json

from copy import deepcopy

from HearthstoneAI import evaluation_utils
from HearthstoneAI.action_tree import get_new_state, get_random_state
from HearthstoneAI.actions_generation import get_cards_play_combinations, get_cards_to_play
from HearthstoneAI.cards import Hero
from HearthstoneAI.cards_generator import card_from_json
from HearthstoneAI.mcts import select_node, sim, back_propagation
from HearthstoneAI.state import Player, State
from settings import CARDS_FILE

i = 0
color = True


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

        self.state.current_player.mana = 1
        np.random.seed(0)
        s, p = get_random_state(self.state)
        print(p)

    def test_mtcs(self):
        deck1 = [deepcopy(self.selfless_hero),
                 deepcopy(self.divine_favor),
                 deepcopy(self.abusive_sergeant),
                 deepcopy(self.agent_squire),
                 deepcopy(self.seal_of_champions),
                 deepcopy(self.steward_of_darshire),
                 deepcopy(self.blessing_of_kings),
                 deepcopy(self.divine_strength),
                 deepcopy(self.wolfrider),
                 deepcopy(self.defender_of_argus)]

        deck2 = [deepcopy(self.abusive_sergeant),
                 deepcopy(self.defender_of_argus),
                 deepcopy(self.divine_favor),
                 deepcopy(self.seal_of_champions),
                 deepcopy(self.agent_squire),
                 deepcopy(self.divine_strength),
                 deepcopy(self.selfless_hero),
                 deepcopy(self.blessing_of_kings),
                 deepcopy(self.wolfrider),
                 deepcopy(self.steward_of_darshire)]
        deck1 = deck1[::-1]
        deck2 = deck2[::-1]

        self.first_player.deck = deck1
        self.second_player.deck = deck2

        self.state.draw_card()
        self.state.draw_card()
        self.state.switch_players()

        self.state.draw_card()
        self.state.draw_card()
        self.state.draw_card()
        self.state.switch_players()

        self.assertEqual(len(self.state.current_player.hand), 2)
        self.assertEqual(len(self.state.current_player.board), 0)
        self.assertEqual(len(self.state.current_player.graveyard), 0)

        self.assertEqual(len(self.state.opposite_player.hand), 3)
        self.assertEqual(len(self.state.opposite_player.board), 0)
        self.assertEqual(len(self.state.opposite_player.graveyard), 0)

        self.assertEqual(self.state.current_player.mana, 1)

        np.random.seed(0)

        root = {'wins': 0,
                'losses': 0,
                'state': self.state,
                'children': [],
                'path': '',
                'parent': None}
        import graphviz as gv

        graph = gv.Graph(format='svg')
        graph.node(name=str(0), label="{} / {}".format(root['wins'], root['wins'] + root['losses']), color=get_color(color))
        graph.render(filename='graph_{}'.format(0))

        for k in range(1, 30):
            selected = select_node(None, root)
            win = sim(selected)
            back_propagation(selected, win)
            print("Win = {}".format(win))

            i = 0
            graph = gv.Graph(format='svg')
            graph.node(name=str(i), label="{} / {}".format(root['wins'], root['wins'] + root['losses']), color=get_color(color))
            graph.render(filename='graph_{}'.format(k))
            for child in root['children']:
                if child['wins'] + child['losses'] > 0:
                    preorder(node=child, graph=graph, parent_name=i, parent_color=color)
            graph.render(filename='graph_{}'.format(k))


        # perform_mcts({'wins': 0, 'losses': 0, 'state': self.state,
        #               'children': [], 'path': '', 'new_turn': True, 'parent': None})

        #
        # root['children'][0]['children'] = [{'wins': 0,
        #                                     'losses': 0,
        #                                     'state': self.state,
        #                                     'children': [],
        #                                     'path': '',
        #                                     'parent': None}, {'wins': 0,
        #                                                       'losses': 0,
        #                                                       'state': self.state,
        #                                                       'children': [],
        #                                                       'path': '',
        #                                                       'parent': None}]
        #
        # root['children'][1]['children'] = [{'wins': 0,
        #                                     'losses': 0,
        #                                     'state': self.state,
        #                                     'children': [],
        #                                     'path': '',
        #                                     'parent': None},
        #                                    {'wins': 0,
        #                                     'losses': 0,
        #                                     'state': self.state,
        #                                     'children': [],
        #                                     'path': '',
        #                                     'parent': None}]
        #
        # root['children'][1]['children'][0]['children'] = [{'wins': 0,
        #                                     'losses': 0,
        #                                     'state': self.state,
        #                                     'children': [],
        #                                     'path': '',
        #                                     'parent': None},
        #                                    {'wins': 0,
        #                                     'losses': 0,
        #                                     'state': self.state,
        #                                     'children': [],
        #                                     'path': '',
        #                                     'parent': None}]
        #


def get_color(parent_color):
    return 'green' if parent_color else 'red'


def preorder(node, graph, parent_name, parent_color):
    global i
    global color
    i += 1
    new_parent = i
    new_parent_color = not parent_color
    s = "{} / {}".format(node['wins'], node['wins'] + node['losses'])
    # print("Node = {}, parent = {}".format(i, parent))
    graph.node(name=str(i), label=s, color=get_color(not parent_color))
    graph.edge(str(parent_name), str(i))
    for n in node['children']:
        if n['wins'] + n['losses'] > 0:
            preorder(n, graph, new_parent, new_parent_color)

