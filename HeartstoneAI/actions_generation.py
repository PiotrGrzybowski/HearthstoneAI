import numpy as np


class Card:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


def get_dubdrtd(cards, target, partial=None, partial_sum=0):
    if partial is None:
        partial = []
    if partial_sum <= target:
        yield partial
    if partial_sum >= target:
        return
    for i, card in enumerate(cards):
        remaining = cards[i + 1:]
        yield from get_dubdrtd(remaining, target, partial + [card.name], partial_sum + card.cost)


def get_cards_play_combinations(cards, indexes, target, partial=None, partial_sum=0):
    if partial is None:
        partial = []
    if partial_sum <= target:
        yield partial
    if partial_sum >= target:
        return
    i = 0

    for ind, c in zip(indexes, cards):
        remaining = cards[i + 1:]
        remaining_indexes = indexes[i + 1:]
        i += 1
        yield from get_cards_play_combinations(remaining, remaining_indexes, target, partial + [ind], partial_sum + c.cost)


if __name__ == "__main__":
    cards = [Card('6', 6), Card('1a', 1), Card('1b', 1), Card('2', 2), Card('3', 3)]
    ind = np.arange(len(cards))

    for c in get_cards_play_combinations(cards, ind, 6):
        print("Score = {}".format(c))

    # print(list(get_possible_cards_play(cards, 1)))
