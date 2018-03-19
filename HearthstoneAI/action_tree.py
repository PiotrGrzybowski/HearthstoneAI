from copy import deepcopy
import random

from HearthstoneAI.cards import Minion, Spell

MAX_MINIONS = 7


def get_leafs(state):
    leafs = []
    walk(state, 0, state.current_player.mana, leafs)
    leafs = set(leafs)
    # print('hey')
    return leafs


def get_new_state(state, evaluation_function):
    leafs = get_leafs(state)
    best_state = state
    max = evaluation_function(best_state)
    path = ''
    for elem in leafs:
        evaluation = evaluation_function(elem[0])
        # print(elem[1])
        if evaluation > max:
            best_state = elem[0]
            path = elem[1]
            max = evaluation
    # print("Path = {}".format(path))
    return best_state, path


def get_random_state(state):
    state, path = walk_random(state, 0, state.current_player.mana)
    return state, path + 'END'


def walk(state, current_mana, available_mana, leafs, lol='', path=''):
    if not state.current_player.hand:
        return walk_attacks(state, leafs, lol, path)
    for index, card in enumerate(state.current_player.hand):
        if card.cost + current_mana <= available_mana \
                and ((is_minion(card) and len(state.current_player.board) < MAX_MINIONS)
                     or isinstance(card, Spell)):
            new_state = deepcopy(state)
            new_path = path + 'Play ' + card.name + ' -> '
            # print(lol + 'Play ' + card.name)
            new_state.play_card(index)
            current_mana += card.cost
            walk(new_state, current_mana, available_mana, leafs, lol + '\t', new_path)
    return walk_attacks(state, leafs, lol, path)


def walk_random(state, current_mana, available_mana, log='', path=''):
    if not state.current_player.hand:
        return walk_attacks_random(state, log, path)

    available_cards = {index: card for index, card in enumerate(state.current_player.hand) if card.cost + current_mana <= available_mana}

    if random.uniform(0, 1) < len(available_cards) / (len(available_cards) + 1):
        new_state = deepcopy(state)
        index, card = random.choice(list(available_cards.items()))
        if (is_minion(card) and len(new_state.current_player.board) < MAX_MINIONS) \
                or isinstance(card, Spell):
            new_path = path + 'Play ' + card.name + ' -> '
            new_state.play_card(index)
            state, path = walk_random(new_state, current_mana + card.cost, available_mana, log + '\t', new_path)
    return walk_attacks_random(state, log, path)


def can_attack(card):
    return isinstance(card, Minion) and not card.summoning_sickness


def is_minion(card):
    return isinstance(card, Minion)


def walk_attacks_random(state, log='', path=''):
    available_cards = {index: card for index, card in enumerate(state.current_player.board) if can_attack(card)}
    cards_to_attack = {index: card for index, card in enumerate(state.opposite_player.board) if is_minion(card)}

    available_actions = (len(available_cards)*(len(cards_to_attack) + 1)) + 1
    attack_options = available_actions - 1

    if attack_options > 0 and random.uniform(0, 1) < attack_options / available_actions:
        new_state = deepcopy(state)
        if random.uniform(0, 1) < len(available_cards) / (available_actions - 1):
            index, card = random.choice(list(available_cards.items()))
            new_path = path + 'Attacking HERO with ' + card.name + ' -> '
            new_state.attack_hero(index)
            state, path = walk_attacks_random(new_state, log + '\t', new_path)
        else:
            index, card = random.choice(list(available_cards.items()))
            opponent_index, opponent_card = random.choice(list(cards_to_attack.items()))
            new_path = path + 'battling ' + card.name + ' and ' + opponent_card.name + ' -> '
            new_state.attack_by_ref(new_state.current_player.board[index],
                                    new_state.opposite_player.board[opponent_index])
            state, path = walk_attacks_random(new_state, log + '\t', new_path)
    return state, path


def walk_attacks(state, leafs, lol='', path=''):
    for index, card in enumerate(state.current_player.board):
        if isinstance(card, Minion) and not card.summoning_sickness:
            new_state = deepcopy(state)
            current_card = new_state.current_player.board[index]
            if current_card in new_state.current_player.board and not current_card.summoning_sickness:
                path += 'Attacking HERO with ' + card.name + ' -> '
                # print(lol + 'Attacking HERO with ' + card.name)
                new_state.attack_hero_by_ref(current_card)
                state, path = walk_attacks(new_state, leafs, lol + '\t', path)
            for opponent_card in new_state.opposite_player.board:
                if isinstance(opponent_card, Minion) and not current_card.summoning_sickness:
                    path += 'battling ' + card.name + ' and ' + opponent_card.name + ' -> '
                    # print(lol + 'battling ' + card.name + ' and ' + opponent_card.name)
                    new_state.attack_by_ref(new_state.current_player.board[index], opponent_card)
                    state, path = walk_attacks(new_state, leafs, lol + '\t', path)
            # newer_state = deepcopy(state)
    path += 'END'
    # print(path)
    leafs.append((state, path))
    return state, path
