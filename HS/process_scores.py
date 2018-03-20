import os
import pickle
import numpy as np

paths = ['/home/piotr/Workspace/Projets/HearthstoneAI/HS/mcts_vs_offensive/',
         '/home/piotr/Workspace/Projets/HearthstoneAI/HS/mcts_vs_passive/',
         '/home/piotr/Workspace/Projets/HearthstoneAI/HS/mcts_vs_random/',
         '/home/piotr/Workspace/Projets/HearthstoneAI/HS/offensive_vs_mcts/',
         '/home/piotr/Workspace/Projets/HearthstoneAI/HS/passive_vs_mcts/',
         '/home/piotr/Workspace/Projets/HearthstoneAI/HS/random_vs_mcts/']

for path in paths:
    how_many_games = 0
    how_many_turns = []
    how_many_root_wins = []
    how_many_root_losses = []
    how_many_child_wins = []
    how_many_child_losses = []
    how_many_visited_nodes = []
    how_many_mcts_win = 0


    for pkl in os.listdir(path):
        with open(os.path.join(path, pkl), "rb") as f:
            load = pickle.load(f)
            turns, root_wins, root_loses, best_child_wins, best_child_losses, visited_nodes, mcts_win = load
            # print(root_wins)
            how_many_games += len(turns)
            how_many_turns += turns
            how_many_root_wins += sum(root_wins, [])
            how_many_root_losses += sum(root_loses, [])
            how_many_child_wins += sum(best_child_wins, [])
            how_many_child_losses += sum(best_child_losses, [])
            how_many_visited_nodes += sum(visited_nodes, [])
            how_many_mcts_win += np.sum(mcts_win)

    result = {'games': how_many_games,
              'mcts_win': how_many_mcts_win,
              'visited_nodes': [np.mean(how_many_visited_nodes), np.std(how_many_visited_nodes)],
              'root_wins': [np.mean(how_many_root_wins), np.std(how_many_root_wins)],
              'root_losses': [np.mean(how_many_root_losses), np.std(how_many_root_losses)],
              'best_child_wins': [np.mean(how_many_child_wins), np.std(how_many_child_wins)],
              'best_child_losses': [np.mean(how_many_child_losses), np.std(how_many_child_losses)]
              }
    print("Type: {}".format(path.split('/')[-2]))
    for k, v in sorted(result.items()):
        print("{}: {}".format(k, v))
    print("="*50)
    print()


