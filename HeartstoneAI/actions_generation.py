class Card:
    def __init__(self, name, value):
        self.name = name
        self.value = value


def subset_sum_cards(cards, target, partial=None, partial_sum=0):
    if partial is None:
        partial = []
    if partial_sum <= target:
        yield partial
    if partial_sum >= target:
        return
    for i, card in enumerate(cards):
        remaining = cards[i + 1:]
        yield from subset_sum_cards(remaining, target, partial + [card.name], partial_sum + card.value)


if __name__ == "__main__":
    cards = [Card('1a', 1), Card('1b', 1), Card('2', 2), Card('3', 3), Card('6', 6)]

    for c in subset_sum_cards(cards, 6):
        print(c)
