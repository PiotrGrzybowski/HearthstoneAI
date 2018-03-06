import numpy as np


def offensive_strategy(state):
    return (20 - state.opposite_player.hero.health) * 10 + sum([minion.attack for minion in state.current_player.board])


def passive_strategy(state):
    player_board = state.current_player.board
    opponent_board = state.opposite_player.board

    return (8 - len(opponent_board) * 10) + len(player_board) * 10 + sum(
        [minion.health for minion in state.current_player.board])


def random_strategy(state):
    return np.random.randint(0, 100)
