from copy import deepcopy

from HearthstoneAI.cards import Minion


def get_leafs(state, available_mana):
    leafs = []
    walk(state, 0, available_mana, leafs)
    return leafs


def get_new_state(state, available_mana, evaluation_function):
    leafs = get_leafs(state, available_mana)
    best_state = state
    max = evaluation_function(best_state)
    path = ''
    for elem in leafs:
        evaluation = evaluation_function(elem[0])
        if evaluation > max:
            best_state = elem[0]
            path = elem[1]
            max = evaluation
    print(path)
    return best_state


def walk(state, current_mana, available_mana, leafs, lol='', path=''):
    if not state.current_player.hand:
        return walk_attacks(state, leafs, lol, path)
    for index, card in enumerate(state.current_player.hand):
        new_state = deepcopy(state)
        if card.cost + current_mana <= available_mana:
            path += 'Play ' + card.name + ' -> '
            print(lol + 'Play ' + card.name)
            new_state.play_card(index)
            walk(new_state, current_mana + card.cost, available_mana, leafs, lol + '\t', path)
    return walk_attacks(state, leafs, lol)


def walk_attacks(state, leafs, lol='', path=''):
    for index, card in enumerate(state.current_player.board):
        new_state = deepcopy(state)
        if isinstance(card, Minion) and not card.summoning_sickness:
            for opponent_card in new_state.opposite_player.board:
                if isinstance(opponent_card, Minion):
                    path += 'battling ' + card.name + ' and ' + opponent_card.name + ' -> '
                    print(lol + 'battling ' + card.name + ' and ' + opponent_card.name)
                    new_state.attack_by_ref(new_state.current_player.board[index], opponent_card)
                    walk_attacks(new_state, leafs, lol + '\t', path)
            newer_state = deepcopy(state)
            path += 'Attacking HERO with ' + card.name + ' -> '
            print(lol + 'Attacking HERO with ' + card.name)
            newer_state.attack_hero(index)
            walk_attacks(newer_state, leafs, lol + '\t', path)
    path += 'END'
    print(lol + 'END')
    leafs.append((state, path))
    return state, path