from copy import deepcopy
import time

from HearthstoneAI.action_tree import get_leafs, get_random_state
import math

C_VALUE = 0.8


def perform_mcts(node):
    # node['state'].switch_players()
    # node['state'].opposite_player.mana -= 1
    timeout = 10
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        selected = select_node(None, node)
        win = sim(selected)
        back_propagation(selected, win)

    # node['state'].switch_players()
    child = get_best_child(node)
    return child


def select_node(parent_node, current_node):
    current_name = current_node['state'].current_player.hero.name
    if current_node['state'].is_terminal:
        return parent_node

    if not current_node['children']:
        opposite_state = deepcopy(current_node['state'])
        opposite_state.new_turn_for_one_player()
        opposite_name = opposite_state.current_player.hero.name
        current_node['children'] = get_nodes_from_leafs(leafs=get_leafs(opposite_state), parent=current_node)
        # print('\t\tBest move can be done by {}'.format(current_node['children'][0]['state'].current_player.name))
        return current_node['children'][0]
    else:
        possible_options = [x for x in current_node['children'] if x['wins'] == 0 and x['losses'] == 0]
        if possible_options:
            return possible_options[0]
        else:
            best_child = get_best_node(current_node, current_node['children'])
            return select_node(parent_node=current_node, current_node=best_child)


def get_best_child(node):
    best_node = get_best_node(node, node['children'])
    return best_node['state'], best_node['path']


def simulation(node, new_turn=True):
    state = deepcopy(node['state'])
    current_player = True
    while not state.is_terminal:
        state.switch_players()
        current_player = not current_player
        for card in state.current_player.board:
            card.summoning_sickness = False
        if new_turn:
            state.new_turn()
        new_turn = not new_turn
        state = get_random_state(state)
    return False if (state.current_player.hero.health <= 0 and current_player) \
                    or (state.current_player.hero.health > 0 and not current_player) else True


def sim(node):
    state = deepcopy(node['state'])
    node_player = state.current_player
    while not state.is_terminal:
        state, _ = get_random_state(state)
        state.new_turn_for_one_player()

    return node_player.name != state.current_player.name


def back_propagation(node, win):
    while True and node:
        if win:
            node['wins'] += 1
        else:
            node['losses'] += 1
        win = not win
        node = node['parent']


def get_best_node(root, nodes):
    return max([n for n in nodes if n['wins'] + n['losses'] > 0], key=lambda x: get_node_value(root, x))


def get_node_value(root, node):
    return node['wins'] / (node['wins'] + node['losses']) \
           + C_VALUE * (math.sqrt(2 * math.log(root['wins'] + root['losses']) / (node['wins'] + node['losses'])))


def get_nodes_from_leafs(leafs, parent):
    return [{'wins': 0, 'losses': 0, 'path': item[1], 'state': item[0], 'children': [], 'parent': parent}
            for item in set(leafs)]


def get_node_from_state(state):
    return {'wins': 0, 'losses': 0, 'path': '', 'state': state, 'children': [], 'parent': None}