from beautifultable import BeautifulTable

from HearthstoneAI.abilities import get_static_abi, get_desc


def print_state(player_1, player_2):
    player_1_hand = BeautifulTable(max_width=140)
    player_1_board = BeautifulTable(max_width=140)

    player_2_hand = BeautifulTable(max_width=140)
    player_2_board = BeautifulTable(max_width=140)

    print("Player: {}".format(player_1.name))
    print("Health: {}".format(player_1.health))
    print("Mana: {}".format(player_1.mana))
    print("Graveyard: {}".format(', '.join([card.name for card in player_1.graveyard])))


    for card in player_1.hand:
        player_1_hand.append_column(card.name, ['Cost = {}'.format(card.cost), get_static_abi(card), get_desc(card)])
    if player_1_hand:
        print("Hand:")
        print(player_1_hand)
    else:
        print("Hand: Empty")

    for card in player_1.board:
        player_1_board.append_column(card.name, [get_static_abi(card), get_desc(card)])

    if player_1_board:
        print("Board")
        print(player_1_board)
    else:
        print("Board: Empty")

    print()
    for card in player_2.board:
        player_2_board.append_column(card.name, [get_static_abi(card), get_desc(card)])

    if player_2_board:
        print("Board:")
        print(player_2_board)
    else:
        print("Board: Empty")

    for card in player_2.hand:
        player_2_hand.append_column(card.name, ['Cost = {}'.format(card.cost), get_static_abi(card), get_desc(card)])

    if player_2_hand:
        print("Hand:")
        print(player_2_hand)
    else:
        print("Hand: Empty")

    print("Graveyard: {}".format(', '.join([card.name for card in player_2.graveyard])))
    print("Mana: {}".format(player_2.mana))
    print("Health: {}".format(player_2.health))
    print("Player: {}".format(player_2.name))
    print("="*130)