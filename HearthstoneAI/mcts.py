from copy import deepcopy

from HearthstoneAI.action_tree import get_leafs, get_random_state
import math

C_VALUE = 0.5


def perform_mcts(node):
    for i in range(10):
        selected = select_node(None, node)
        for i in range(10):
            win = simulation(selected, selected['new_turn'])
            print(win)
            back_propagation(selected, win)
    print('yahoo')


def select_node(parent_node, current_node):
    if current_node['state'].is_terminal:
        return parent_node

    if not current_node['children']:
        opposite_state = deepcopy(current_node['state'])
        opposite_state.new_turn_for_one_player()
        current_node['children'] = get_nodes_from_leafs(leafs=get_leafs(opposite_state), parent=current_node)
        return current_node['children'][0]
    else:
        possible_options = [x for x in current_node['children'] if x['wins'] == 0 and x['losses'] == 0]
        if possible_options:
            return possible_options[0]
        else:
            best_child = get_best_node(current_node, current_node['children'])
            return select_node(parent_node=current_node, current_node=best_child)


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
        state.new_turn_for_one_player()
        state, _ = get_random_state(state)

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
    return max(nodes, key=lambda x: get_node_value(root, x))


def get_node_value(root, node):
    return node['wins'] / (node['wins'] + node['losses']) \
           + C_VALUE * (math.sqrt(2 * math.log(root['wins'] + root['losses'])
                                  / (node['wins'] + node['losses'])))


def get_nodes_from_leafs(leafs, parent):
    return [{'wins': 0, 'losses': 0, 'path': item[1], 'state': item[0], 'children': [], 'parent': parent}
            for item in set(leafs)]
