class Card:
    def __init__(self, name, cost, abilities):
        self.name = name
        self.cost = cost
        self.abilities = abilities


class CombatCard(Card):
    def __init__(self, name, cost, abilities, attack, health):
        super().__init__(name, cost, abilities)
        self.attack = attack
        self.health = health


class Minion(CombatCard):
    def __init__(self, name, cost, abilities, attack, health, minion_type):
        super().__init__(name, cost, abilities, attack, health)
        self.minion_type = minion_type


class Hero(CombatCard):
    def __init__(self, name, cost, abilities, attack, health, hero_class):
        super().__init__(name, cost, abilities, attack, health)
        self.hero_class = hero_class


class Spell(Card):
    def __init__(self, name, cost, abilities):
        super().__init__(name, cost, abilities)


class CardPool:
    def __init__(self, cards, max_size):
        self.cards = cards
        self.max_size = max_size
