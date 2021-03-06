SPELL = 'Spell'
MINION = 'Minion'


class Card:
    def __init__(self, name, cost, abilities):
        self.name = name
        self.cost = cost
        self.abilities = abilities

    def __hash__(self):
        return hash((self.name, self.cost))


class CombatCard(Card):
    def __init__(self, name, cost, abilities, attack, health):
        super().__init__(name, cost, abilities)
        self.attack = attack
        self.health = health

    def __hash__(self):
        return hash((self.name, self.cost,
                     self.attack, self.health))


class Minion(CombatCard):
    def __init__(self, name, cost, abilities, attack, health, minion_type):
        super().__init__(name, cost, abilities, attack, health)
        self.minion_type = minion_type
        self.summoning_sickness = True

    def __hash__(self):
        return hash((self.name, self.cost,
                     self.attack, self.health,
                     self.minion_type, self.summoning_sickness))


class Hero(CombatCard):
    def __init__(self, name, cost, abilities, attack, health, hero_class):
        super().__init__(name, cost, abilities, attack, health)
        self.hero_class = hero_class

    def __hash__(self):
        return hash((self.name, self.cost,
                     self.attack, self.health,
                     self.hero_class))


class Spell(Card):
    def __init__(self, name, cost, abilities):
        super().__init__(name, cost, abilities)


CARD_TYPES = {MINION: Minion,
              SPELL: Spell}
