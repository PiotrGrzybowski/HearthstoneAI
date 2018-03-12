from copy import deepcopy

from HearthstoneAI.action_tree import get_leafs, get_random_state
import math

C_VALUE = 0.5


def perform_mcts(node):
    node['state'].mana = 3
    for i in range(10):
        selected = select_node(None, node)
        for i in range(10):
            win = simulate(selected, selected['new_turn'])
            print(win)
            backprop(selected, win)
    print('yahoo')


def select_node(parent_node, current_node):
    if current_node['state'].is_terminal:
        return parent_node
    if not current_node['children']:
        opposite_state = deepcopy(current_node['state'])
        if current_node['new_turn']:
            opposite_state.new_turn()
        opposite_state.switch_players()
        current_node['children'] = get_nodes(content=get_leafs(opposite_state), parent=current_node,
                                             new_turn=not current_node['new_turn'])
        return current_node['children'][0]
    else:
        possible_options = [x for x in current_node['children'] if x['wins'] == 0 and x['losses'] == 0]
        if possible_options:
            return possible_options[0]
        else:
            best_child = get_best_node(current_node, current_node['children'])
            return select_node(parent_node=current_node, current_node=best_child)


def simulate(node, new_turn=True):
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
        state = get_random_state(state, state.mana)
    return False if (state.current_player.hero.health <= 0 and current_player) \
                    or (state.current_player.hero.health > 0 and not current_player) else True


def backprop(node, win):
    while True:
        if win:
            node['wins'] += 1
        else:
            node['losses'] += 1
        win = not win
        node = node['parent']
        if node is None:
            break


def get_best_node(root, nodes):
    return max(nodes, key=lambda x: get_node_value(root, x))


def get_node_value(root, node):
    return node['wins'] / (node['wins'] + node['losses']) \
           + C_VALUE * (math.sqrt(2 * math.log(root['wins'] + root['losses'])
                                  / (node['wins'] + node['losses'])))


def get_nodes(content, parent, new_turn):
    states = set(content)
    result = []
    for item in states:
        elem = dict()
        elem['wins'] = 0
        elem['losses'] = 0
        elem['path'] = item[1]
        elem['state'] = item[0]
        elem['children'] = []
        elem['new_turn'] = new_turn
        elem['parent'] = parent
        result.append(elem)
    return result


def pamisio_get_nodes(content, parent, new_turn):
    return [{'wins': 0, 'losses': 0, 'path': item[1],
             'state': item[0], 'children': [], 'new_turn': new_turn, 'parent': parent} for item in set(content)]
