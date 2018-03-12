from copy import deepcopy
import random

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
        # print(elem[1])
        if evaluation > max:
            best_state = elem[0]
            path = elem[1]
            max = evaluation
    print("Path = {}".format(path))
    return best_state


def get_random_state(state, available_mana):
    state, path = walk_random(state, 0, available_mana)
    # print("Path = {}".format(path))
    return state


def walk(state, current_mana, available_mana, leafs, lol='', path=''):
    if not state.current_player.hand:
        return walk_attacks(state, leafs, lol, path)
    for index, card in enumerate(state.current_player.hand):
        new_state = deepcopy(state)
        if card.cost + current_mana <= available_mana:
            path += 'Play ' + card.name + ' -> '
            # print(lol + 'Play ' + card.name)
            new_state.play_card(index)
            current_mana += card.cost
            walk(new_state, current_mana, available_mana, leafs, lol + '\t', path)
    return walk_attacks(state, leafs, lol, path)


def walk_random(state, current_mana, available_mana, log='', path=''):
    if not state.current_player.hand:
        return walk_attacks_random(state, log, path)
    available_cards = dict()
    for index, card in enumerate(state.current_player.hand):
        if card.cost + current_mana <= available_mana:
            available_cards[index] = card
    if random.uniform(0, 1) < len(available_cards)/(len(available_cards) + 1):
        new_state = deepcopy(state)
        index, card = random.choice(list(available_cards.items()))
        path += 'Play ' + card.name + ' -> '
        new_state.play_card(index)
        current_mana += card.cost
        state, path = walk_random(new_state, current_mana, available_mana, log + '\t', path)
    return walk_attacks_random(state, log, path)


def walk_attacks_random(state, log='', path=''):
    available_cards = dict() #Why is this a dict not a list?
    for index, card in enumerate(state.current_player.board):
        if isinstance(card, Minion) and not card.summoning_sickness:
            available_cards[index] = card
    cards_to_attack = dict()
    for index, card in enumerate(state.opposite_player.board):
        if isinstance(card, Minion) and not card.summoning_sickness: #Do cards to attack have to have summoning sickness set to False if we want to attack them?
            cards_to_attack[index] = card
    # combinations of our board cards and opponent cards
    # + options of attacking hero with our cards + not doing anything
    available_actions = (len(available_cards)*(len(cards_to_attack) + 1)) + 1
    attack_options = available_actions - 1
    if available_actions - 1 > 0 and random.uniform(0, 1) < attack_options / available_actions: #Why jus no andom.uniform(0, 1) < 0.5?
        new_state = deepcopy(state)
        if random.uniform(0, 1) < len(available_cards) / (available_actions - 1):
            index, card = random.choice(list(available_cards.items()))
            path += 'Attacking HERO with ' + card.name + ' -> '
            new_state.attack_hero(index)
            state, path = walk_attacks_random(new_state, log + '\t', path)
        else:
            index, card = random.choice(list(available_cards.items()))
            opponent_index, opponent_card = random.choice(list(cards_to_attack.items()))
            path += 'battling ' + card.name + ' and ' + opponent_card.name + ' -> '
            new_state.attack_by_ref(new_state.current_player.board[index],
                                    new_state.opposite_player.board[opponent_index])
            state, path = walk_attacks_random(new_state, log + '\t', path)
    return state, path


def walk_attacks(state, leafs, lol='', path=''):
    for index, card in enumerate(state.current_player.board):
        new_state = deepcopy(state)
        current_card = new_state.current_player.board[index]
        if isinstance(card, Minion) and not card.summoning_sickness:
            if current_card in new_state.current_player.board and not current_card.summoning_sickness:
                path += 'Attacking HERO with ' + card.name + ' -> '
                # print(lol + 'Attacking HERO with ' + card.name)
                new_state.attack_hero_by_ref(current_card)
                walk_attacks(new_state, leafs, lol + '\t', path)
            for opponent_card in new_state.opposite_player.board:
                if isinstance(opponent_card, Minion) and not current_card.summoning_sickness:
                    path += 'battling ' + card.name + ' and ' + opponent_card.name + ' -> '
                    # print(lol + 'battling ' + card.name + ' and ' + opponent_card.name)
                    new_state.attack_by_ref(new_state.current_player.board[index], opponent_card)
                    walk_attacks(new_state, leafs, lol + '\t', path)
            # newer_state = deepcopy(state)
    path += 'END'
    # print(lol + 'END')
    leafs.append((state, path))
    return state, path
