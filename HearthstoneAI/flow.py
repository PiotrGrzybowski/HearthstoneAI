from functools import partial
from random import shuffle
import json
from HearthstoneAI import evaluation_utils
from HearthstoneAI.action_tree import get_new_state, get_random_state, get_leafs
from HearthstoneAI.cards import Hero
from HearthstoneAI.cards_generator import card_from_json
from HearthstoneAI.gui import print_state
from HearthstoneAI.mcts import perform_mcts, get_node_from_state
from HearthstoneAI.state import Player, State
from settings import CARDS_FILE
import numpy as np
import pickle


def deals_manage_to_opposite_player(state, damage):
    state.opposite_player.hero.health -= damage


ability = partial(deals_manage_to_opposite_player, damage=2)


def build_decks():
    deck1 = []
    deck2 = []
    with open(CARDS_FILE) as json_file:
        data = json.load(json_file)
        for card in data:
            deck1.append(card_from_json(card))
            deck1.append(card_from_json(card))
            deck2.append(card_from_json(card))
            deck2.append(card_from_json(card))
    shuffle(deck1)
    shuffle(deck2)
    return deck1, deck2


def round(state):
    state.draw_card()
    state.play_card(3)
    state.attack(2, 3)


def change_turn(state, mana):
    mana += 1 if mana < 10 else 0
    state.switch_players()
    state.disable_sickness()


def game():
    deck1, deck2 = build_decks()
    hero_1 = Hero(name='Pamisio', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)
    hero_2 = Hero(name='Pamewcia', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)

    first_player = Player(hero_1, [], deck1, [], [])
    second_player = Player(hero_2, [], deck2, [], [])
    state = State(first_player, second_player)

    for i in range(2):
        state.draw_card()

    state.switch_players()

    for i in range(3):
        state.draw_card()

    state.switch_players()

    for mana in range(1, 10):
        state.draw_card()
        print("Player {}".format(1))
        print("Hand: {}".format([(minion.name, minion.cost) for minion in state.current_player.hand]))
        for card in state.current_player.board:
            card.summoning_sickness = False
        state = get_new_state(state, mana, evaluation_utils.offensive_strategy)
        print("Player 1 health = {} \nPlayer 2 health = {}".format(state.current_player.hero.health, state.opposite_player.hero.health))
        state.switch_players()

        state.draw_card()
        print("\nPlayer {}".format(2))
        print("Hand: {}".format([(minion.name, minion.cost) for minion in state.current_player.hand]))
        for card in state.current_player.board:
            card.summoning_sickness = False
        state = get_new_state(state, mana, evaluation_utils.offensive_strategy)
        print("Player 1 health = {} \nPlayer 2 health = {}".format(state.current_player.hero.health, state.opposite_player.hero.health))
        state.switch_players()

        print("\n----------------\n")

        if state.is_terminal:
            break


def random_playoff():
    deck1, deck2 = build_decks()
    hero_1 = Hero(name='Pamisio', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)
    hero_2 = Hero(name='Pamewcia', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)

    first_player = Player(hero_1, [], deck1, [], [])
    second_player = Player(hero_2, [], deck2, [], [])
    state = State(first_player, second_player)

    for i in range(2):
        state.draw_card()

    state.switch_players()

    for i in range(3):
        state.draw_card()

    state.switch_players()

    for mana in range(1, 10):
        state.draw_card()
        print("Player {}".format(1))
        print("Hand: {}".format([(minion.name, minion.cost) for minion in state.current_player.hand]))
        for card in state.current_player.board:
            card.summoning_sickness = False
        state = get_random_state(state, mana)
        print("Player 1 health = {} \nPlayer 2 health = {}".format(state.current_player.hero.health,
                                                                   state.opposite_player.hero.health))

        if state.is_terminal:
            break

        state.switch_players()

        state.draw_card()
        print("\nPlayer {}".format(2))
        print("Hand: {}".format([(minion.name, minion.cost) for minion in state.current_player.hand]))
        for card in state.current_player.board:
            card.summoning_sickness = False
        state = get_random_state(state, mana)
        print("Player 1 health = {} \nPlayer 2 health = {}".format(state.opposite_player.hero.health,
                                                                   state.current_player.hero.health))
        state.switch_players()

        print("\n----------------\n")

        if state.is_terminal:
            break


def play_start_agent_passive_vs_mcts():
    deck1, deck2 = build_decks()
    hero_1 = Hero(name='Agent', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)
    hero_2 = Hero(name='MCTS', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)

    first_player = Player(hero_1, [], deck1, [], [])
    second_player = Player(hero_2, [], deck2, [], [])
    state = State(first_player, second_player)

    state.draw_card()
    state.draw_card()
    state.switch_players()

    state.draw_card()
    state.draw_card()
    state.draw_card()

    turns = 1
    root_wins = []
    root_loses = []
    best_child_wins = []
    best_child_losses = []
    visited_nodes = []

    while not state.is_terminal:
        state.new_turn_for_one_player()
        # state, path = get_random_state(state)
        state, path = get_new_state(state, evaluation_utils.passive_strategy)
        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))
        if state.is_terminal:
            break

        start_node = get_node_from_state(state)
        best_child = perform_mcts(start_node)
        state, path = best_child['state'], best_child['path']
        root_wins.append(start_node['wins'])
        root_loses.append(start_node['losses'])
        best_child_wins.append(best_child['wins'])
        best_child_losses.append(best_child['losses'])
        visited_nodes.append(start_node['wins'] + start_node['losses'])

        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))
        turns += 1
        visited_nodes.append(start_node['wins'] + start_node['losses'])
    mcts_win = 1 if state.get_player_by_name('Agent').health == 0 else 0
    print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))

    return turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win


def play_start_agent_offensive_vs_mcts():
    deck1, deck2 = build_decks()
    hero_1 = Hero(name='Agent', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)
    hero_2 = Hero(name='MCTS', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)

    first_player = Player(hero_1, [], deck1, [], [])
    second_player = Player(hero_2, [], deck2, [], [])
    state = State(first_player, second_player)

    state.draw_card()
    state.draw_card()
    state.switch_players()

    state.draw_card()
    state.draw_card()
    state.draw_card()

    turns = 1
    root_wins = []
    root_loses = []
    best_child_wins = []
    best_child_losses = []
    visited_nodes = []

    while not state.is_terminal:
        state.new_turn_for_one_player()
        # state, path = get_random_state(state)
        state, path = get_new_state(state, evaluation_utils.offensive_strategy)
        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))
        if state.is_terminal:
            break

        start_node = get_node_from_state(state)
        best_child = perform_mcts(start_node)
        state, path = best_child['state'], best_child['path']
        root_wins.append(start_node['wins'])
        root_loses.append(start_node['losses'])
        best_child_wins.append(best_child['wins'])
        best_child_losses.append(best_child['losses'])
        visited_nodes.append(start_node['wins'] + start_node['losses'])

        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))
        turns += 1
        visited_nodes.append(start_node['wins'] + start_node['losses'])
    mcts_win = 1 if state.get_player_by_name('Agent').health == 0 else 0
    print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))

    return turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win


def play_start_agent_random_vs_mcts():
    deck1, deck2 = build_decks()
    hero_1 = Hero(name='Agent', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)
    hero_2 = Hero(name='MCTS', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)

    first_player = Player(hero_1, [], deck1, [], [])
    second_player = Player(hero_2, [], deck2, [], [])
    state = State(first_player, second_player)

    state.draw_card()
    state.draw_card()
    state.switch_players()

    state.draw_card()
    state.draw_card()
    state.draw_card()

    turns = 1
    root_wins = []
    root_loses = []
    best_child_wins = []
    best_child_losses = []
    visited_nodes = []

    while not state.is_terminal:
        state.new_turn_for_one_player()
        state, path = get_random_state(state)
        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))
        if state.is_terminal:
            break

        start_node = get_node_from_state(state)
        best_child = perform_mcts(start_node)
        state, path = best_child['state'], best_child['path']
        root_wins.append(start_node['wins'])
        root_loses.append(start_node['losses'])
        best_child_wins.append(best_child['wins'])
        best_child_losses.append(best_child['losses'])
        visited_nodes.append(start_node['wins'] + start_node['losses'])

        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))
        turns += 1
        visited_nodes.append(start_node['wins'] + start_node['losses'])
    mcts_win = 1 if state.get_player_by_name('Agent').health == 0 else 0
    print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))

    return turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win


def start_mcts_vs_random():
    deck1, deck2 = build_decks()
    hero_1 = Hero(name='MCTS', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)
    hero_2 = Hero(name='Agent', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)

    first_player = Player(hero_1, [], deck1, [], [])
    second_player = Player(hero_2, [], deck2, [], [])
    state = State(first_player, second_player)

    state.draw_card()
    state.draw_card()
    state.switch_players()

    state.draw_card()
    state.draw_card()
    state.draw_card()

    turns = 1
    root_wins = []
    root_loses = []
    best_child_wins = []
    best_child_losses = []
    visited_nodes = []

    while not state.is_terminal:
        # state.new_turn_for_one_player()
        # state.switch_players()
        start_node = get_node_from_state(state)
        best_child = perform_mcts(start_node)
        state, path = best_child['state'], best_child['path']
        root_wins.append(start_node['wins'])
        root_loses.append(start_node['losses'])
        best_child_wins.append(best_child['wins'])
        best_child_losses.append(best_child['losses'])
        visited_nodes.append(start_node['wins'] + start_node['losses'])

        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))
        if state.is_terminal:
            break

        state.new_turn_for_one_player()
        state, path = get_random_state(state)
        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))

        turns += 1

    mcts_win = 1 if state.get_player_by_name('Agent').health == 0 else 0
    print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))

    return turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win


def start_mcts_vs_offensive():
    deck1, deck2 = build_decks()
    hero_1 = Hero(name='MCTS', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)
    hero_2 = Hero(name='Agent', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)

    first_player = Player(hero_1, [], deck1, [], [])
    second_player = Player(hero_2, [], deck2, [], [])
    state = State(first_player, second_player)

    state.draw_card()
    state.draw_card()
    state.switch_players()

    state.draw_card()
    state.draw_card()
    state.draw_card()

    turns = 1
    root_wins = []
    root_loses = []
    best_child_wins = []
    best_child_losses = []
    visited_nodes = []

    while not state.is_terminal:
        # state.new_turn_for_one_player()
        # state.switch_players()
        start_node = get_node_from_state(state)
        best_child = perform_mcts(start_node)
        state, path = best_child['state'], best_child['path']
        root_wins.append(start_node['wins'])
        root_loses.append(start_node['losses'])
        best_child_wins.append(best_child['wins'])
        best_child_losses.append(best_child['losses'])
        visited_nodes.append(start_node['wins'] + start_node['losses'])

        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))
        if state.is_terminal:
            break

        state.new_turn_for_one_player()
        state, path = get_new_state(state, evaluation_utils.offensive_strategy)
        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))

        turns += 1

    mcts_win = 1 if state.get_player_by_name('Agent').health == 0 else 0
    print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))

    return turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win


def start_mcts_vs_passive():
    deck1, deck2 = build_decks()
    hero_1 = Hero(name='MCTS', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)
    hero_2 = Hero(name='Agent', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)

    first_player = Player(hero_1, [], deck1, [], [])
    second_player = Player(hero_2, [], deck2, [], [])
    state = State(first_player, second_player)

    state.draw_card()
    state.draw_card()
    state.switch_players()

    state.draw_card()
    state.draw_card()
    state.draw_card()

    turns = 1
    root_wins = []
    root_loses = []
    best_child_wins = []
    best_child_losses = []
    visited_nodes = []

    while not state.is_terminal:
        # state.new_turn_for_one_player()
        # state.switch_players()
        start_node = get_node_from_state(state)
        best_child = perform_mcts(start_node)
        state, path = best_child['state'], best_child['path']
        root_wins.append(start_node['wins'])
        root_loses.append(start_node['losses'])
        best_child_wins.append(best_child['wins'])
        best_child_losses.append(best_child['losses'])
        visited_nodes.append(start_node['wins'] + start_node['losses'])

        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))
        if state.is_terminal:
            break

        state.new_turn_for_one_player()
        state, path = get_new_state(state, evaluation_utils.passive_strategy)
        #print("\n\nAction taken by {}: {}\n\n".format(state.current_player.name, path))
        print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))

        turns += 1

    mcts_win = 1 if state.get_player_by_name('Agent').health == 0 else 0
    print_state(state.get_player_by_name(hero_1.name), state.get_player_by_name(hero_2.name))

    return turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win


if __name__ == "__main__":
    print("Game")
    games_to_play = 5
    turns_list = []
    root_wins_list = []
    root_loses_list = []
    best_child_wins_list = []
    best_child_losses_list = []
    visited_nodes_list = []
    mcts_win_list = []

    for i in range(games_to_play):
        print("{} game mtcs vs ranodm".format(i))
        turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win = start_mcts_vs_random()
        turns_list.append(turns)
        root_wins_list.append(root_wins)
        root_loses_list.append(root_loses)
        best_child_wins_list.append(best_child_wins)
        best_child_losses_list.append(best_child_losses)
        visited_nodes_list.append(visited_nodes)
        mcts_win_list.append(mcts_win)

    result = [turns_list, root_wins_list, root_loses_list, best_child_wins_list, best_child_losses_list, visited_nodes_list, mcts_win_list]

    with open('start_mcts_vs_random.pkl', 'wb') as fp:
        pickle.dump(result, fp)

    print("Game")
    turns_list = []
    root_wins_list = []
    root_loses_list = []
    best_child_wins_list = []
    best_child_losses_list = []
    visited_nodes_list = []
    mcts_win_list = []

    for i in range(games_to_play):
        print("{} game mtcs vs offensivem".format(i))
        turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win = start_mcts_vs_offensive()
        turns_list.append(turns)
        root_wins_list.append(root_wins)
        root_loses_list.append(root_loses)
        best_child_wins_list.append(best_child_wins)
        best_child_losses_list.append(best_child_losses)
        visited_nodes_list.append(visited_nodes)
        mcts_win_list.append(mcts_win)

    result = [turns_list, root_wins_list, root_loses_list, best_child_wins_list, best_child_losses_list,
              visited_nodes_list, mcts_win_list]

    with open('start_mcts_vs_offensive.pkl', 'wb') as fp:
        pickle.dump(result, fp)

    print("Game")
    turns_list = []
    root_wins_list = []
    root_loses_list = []
    best_child_wins_list = []
    best_child_losses_list = []
    visited_nodes_list = []
    mcts_win_list = []

    for i in range(games_to_play):
        print("{} game mtcs vs passive".format(i))
        turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win = start_mcts_vs_passive()
        turns_list.append(turns)
        root_wins_list.append(root_wins)
        root_loses_list.append(root_loses)
        best_child_wins_list.append(best_child_wins)
        best_child_losses_list.append(best_child_losses)
        visited_nodes_list.append(visited_nodes)
        mcts_win_list.append(mcts_win)

    result = [turns_list, root_wins_list, root_loses_list, best_child_wins_list, best_child_losses_list,
              visited_nodes_list, mcts_win_list]

    with open('start_mcts_vs_passive.pkl', 'wb') as fp:
        pickle.dump(result, fp)

    print("Game")
    turns_list = []
    root_wins_list = []
    root_loses_list = []
    best_child_wins_list = []
    best_child_losses_list = []
    visited_nodes_list = []
    mcts_win_list = []

    for i in range(games_to_play):
        print("{} game passive vs mcts".format(i))

        turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win = play_start_agent_passive_vs_mcts()
        turns_list.append(turns)
        root_wins_list.append(root_wins)
        root_loses_list.append(root_loses)
        best_child_wins_list.append(best_child_wins)
        best_child_losses_list.append(best_child_losses)
        visited_nodes_list.append(visited_nodes)
        mcts_win_list.append(mcts_win)

    result = [turns_list, root_wins_list, root_loses_list, best_child_wins_list, best_child_losses_list,
              visited_nodes_list, mcts_win_list]

    with open('play_start_agent_passive_vs_mcts.pkl', 'wb') as fp:
        pickle.dump(result, fp)

    print("Game")
    turns_list = []
    root_wins_list = []
    root_loses_list = []
    best_child_wins_list = []
    best_child_losses_list = []
    visited_nodes_list = []
    mcts_win_list = []

    for i in range(games_to_play):
        print("{} game ranodom vs mcts".format(i))

        turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win = play_start_agent_offensive_vs_mcts()
        turns_list.append(turns)
        root_wins_list.append(root_wins)
        root_loses_list.append(root_loses)
        best_child_wins_list.append(best_child_wins)
        best_child_losses_list.append(best_child_losses)
        visited_nodes_list.append(visited_nodes)
        mcts_win_list.append(mcts_win)

    result = [turns_list, root_wins_list, root_loses_list, best_child_wins_list, best_child_losses_list,
              visited_nodes_list, mcts_win_list]

    with open('play_start_agent_offensive_vs_mcts.pkl', 'wb') as fp:
        pickle.dump(result, fp)

    print("Game")
    turns_list = []
    root_wins_list = []
    root_loses_list = []
    best_child_wins_list = []
    best_child_losses_list = []
    visited_nodes_list = []
    mcts_win_list = []

    for i in range(games_to_play):
        print("{} game ranodom vs mcts".format(i))

        turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win = splay_start_agent_random_vs_mcts()
        turns_list.append(turns)
        root_wins_list.append(root_wins)
        root_loses_list.append(root_loses)
        best_child_wins_list.append(best_child_wins)
        best_child_losses_list.append(best_child_losses)
        visited_nodes_list.append(visited_nodes)
        mcts_win_list.append(mcts_win)

    result = [turns_list, root_wins_list, root_loses_list, best_child_wins_list, best_child_losses_list,
              visited_nodes_list, mcts_win_list]

    with open('play_start_agent_random_vs_mcts.pkl', 'wb') as fp:
        pickle.dump(result, fp)

    print("Game")

