from HearthstoneAI.action_tree import get_leafs


def perform_mcts(state, mana, cont=True):
    children = uniquify(get_leafs(state, mana))
    print(len(children))
    if cont:
        for item in children:
            perform_mcts(item[0], mana + 1, cont=False)


def uniquify(content):
    return set(content)
