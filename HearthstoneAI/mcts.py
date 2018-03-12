from copy import deepcopy

from HearthstoneAI.action_tree import get_leafs, get_random_state
import math

C_VALUE = 0.5


def perform_mcts(node, mana, next_round=False):
    selected = select_node(node, node, mana)
    win = simulate(selected, mana)


def select_node(parent_node, current_node, mana):
    if current_node['state'].is_terminal:
        return parent_node
    if not current_node['children']:
        opposite_state = deepcopy(current_node['state'])
        opposite_state.switch_players()
        current_node['children'] = get_nodes(get_leafs(opposite_state, mana))
        return current_node['children'][0]
    else:
        possible_options = [x for x in current_node['children'] if x['wins'] == 0 and x['losses'] == 0]
        if possible_options:
            return possible_options[0]
        else:
            best_child = get_best_node(parent_node, current_node['children'])
            return select_node(parent_node, best_child, mana)


def simulate(node, mana, increase_mana=True):
    state = node['state']
    current_player = True
    while not state.is_terminal:
        state.switch_players()
        current_player = not current_player
        for card in state.current_player.board:
            card.summoning_sickness = False
        if increase_mana:
            mana += 1
            state.draw_card()
            state.switch_players()
            state.draw_card()
            state.switch_players()
        increase_mana = not increase_mana
        state = get_random_state(state, mana)
    return False if (state.current_player.hero.health <= 0 and current_player) \
                    or (state.current_player.hero.health > 0 and not current_player) else True


def expand(node):
    pass


def get_best_node(root, nodes):
    return max(nodes, key=lambda x: get_node_value(root, x))


def get_node_value(root, node):
    return node['wins'] / (node['wins'] + node['losses']) \
           + C_VALUE * (math.sqrt(2 * math.log(root['wins'] + root['losses'])
                                  / (node['wins'] + node['losses'])))


def get_nodes(content):
    states = set(content)
    result = []
    for item in states:
        elem = dict()
        elem['wins'] = 0
        elem['losses'] = 0
        elem['path'] = item[1]
        elem['state'] = item[0]
        elem['children'] = []
        result.append(elem)
    return result
