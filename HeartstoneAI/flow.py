from functools import partial


def deals_manage_to_opposite_player(state, damage):
    state.opposite_player.hero.health -= damage

ability = partial(deals_manage_to_opposite_player, damage=2)



