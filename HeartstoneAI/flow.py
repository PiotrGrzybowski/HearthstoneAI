from functools import partial


def deals_manage_to_opposite_player(state, damage):
    state.opposite_player.hero.health -= damage


ability = partial(deals_manage_to_opposite_player, damage=2)


def round(state):
    state.draw_card()
    state.play_card(3)
    state.attack(2, 3)


def change_turn(state, mana):
    mana += 1 if mana < 10 else 0
    state.switch_players()
    state.disable_sickness()

