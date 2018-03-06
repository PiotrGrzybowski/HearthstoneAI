from functools import partial
from random import shuffle
import json
from HearthstoneAI import evaluation_utils
from HearthstoneAI.action_tree import get_new_state
from HearthstoneAI.cards import Hero
from HearthstoneAI.cards_generator import card_from_json
from HearthstoneAI.state import Player, State
from settings import CARDS_FILE


def deals_manage_to_opposite_player(state, damage):
    state.opposite_player.hero.health -= damage


ability = partial(deals_manage_to_opposite_player, damage=2)


def build_decks():
    deck1 = []
    deck2 = []
    with open(CARDS_FILE) as json_file:
        data = json.load(json_file)
        for card in data:
            deck1.append(card_from_json(card))
            deck1.append(card_from_json(card))
            deck2.append(card_from_json(card))
            deck2.append(card_from_json(card))
    shuffle(deck1)
    shuffle(deck2)
    return deck1, deck2


def round(state):
    state.draw_card()
    state.play_card(3)
    state.attack(2, 3)


def change_turn(state, mana):
    mana += 1 if mana < 10 else 0
    state.switch_players()
    state.disable_sickness()


def game():
    deck1, deck2 = build_decks()
    hero_1 = Hero(name='Pamisio', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)
    hero_2 = Hero(name='Pamewcia', cost=0, abilities=dict(), attack=0, health=20, hero_class=None)

    first_player = Player(hero_1, [], deck1, [], [])
    second_player = Player(hero_2, [], deck2, [], [])
    state = State(first_player, second_player)

    for i in range(2):
        state.draw_card()

    state.switch_players()

    for i in range(3):
        state.draw_card()

    state.switch_players()

    for mana in range(1, 10):
        state.draw_card()
        print("Player {}".format(1))
        for card in state.current_player.board:
            card.summoning_sickness = False
        state = get_new_state(state, mana, evaluation_utils.offensive_strategy)
        print("Player 1 health = {}, Player 2 health = {}".format(state.current_player.hero.health, state.opposite_player.hero.health))
        state.switch_players()

        state.draw_card()
        print("\nPlayer {}".format(2))
        for card in state.current_player.board:
            card.summoning_sickness = False
        state = get_new_state(state, mana, evaluation_utils.random_strategy)
        print("Player 1 health = {}, Player 2 health = {}".format(state.current_player.hero.health, state.opposite_player.hero.health))
        state.switch_players()

        print("\n----------------\n")

        if state.is_terminal:
            break



if __name__ == "__main__":
    game()
