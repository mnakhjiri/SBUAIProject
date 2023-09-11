import collections
import math

import numpy as np


def check_win(board_state):
    j = 0
    for col in board_state:
        i = 0
        for cell in col:
            if cell != 0:
                if i >= 3 and (np.array_equal(col[i - 3:i + 1], [cell, cell, cell, cell])):
                    return cell
                if i <= 2 and (np.array_equal(col[i:i + 4], [cell, cell, cell, cell])):
                    return cell
                if j >= 3 and (np.array_equal(board_state[j - 3:j + 1, i], [cell, cell, cell, cell])):
                    return cell
                if j <= 3 and (np.array_equal(board_state[j:j + 4, i], [cell, cell, cell, cell])):
                    return cell
                if i >= 3 and j >= 3:
                    if board_state[j - 1][i - 1] == cell and board_state[j - 2][i - 2] == cell and board_state[j - 3][
                       i - 3] == cell:
                        return cell
                if i <= 2 and j <= 3:
                    if board_state[j + 1][i + 1] == cell and board_state[j + 2][i + 2] == cell and board_state[j + 3][
                       i + 3] == cell:
                        return cell
                if i >= 3 and j <= 3:
                    if board_state[j + 1][i - 1] == cell and board_state[j + 2][i - 2] == cell and board_state[j + 3][
                       i - 3] == cell:
                        return cell
                if i <= 2 and j >= 3:
                    if board_state[j - 1][i + 1] == cell and board_state[j - 2][i + 2] == cell and board_state[j - 3][
                       i + 3] == cell:
                        return cell
            i += 1
        j += 1
    return 0


def get_result_array(board_state):
    j = 0
    for col in board_state:
        i = 0
        for cell in col:
            if cell != 0:
                if i >= 3 and (np.array_equal(col[i - 3:i + 1], [cell, cell, cell, cell])):
                    return [(i - 3, j), (i - 2, j), (i - 1, j), (i, j)]
                if i <= 2 and (np.array_equal(col[i:i + 4], [cell, cell, cell, cell])):
                    return [(i, j), (i + 1, j), (i + 2, j), (i + 3, j)]
                if j >= 3 and (np.array_equal(board_state[j - 3:j + 1, i], [cell, cell, cell, cell])):
                    return [(i, j - 3), (i, j - 2), (i, j - 1), (i, j)]
                if j <= 3 and (np.array_equal(board_state[j:j + 4, i], [cell, cell, cell, cell])):
                    return [(i, j), (i, j + 1), (i, j + 2), (i, j + 3)]
                if i >= 3 and j >= 3:
                    if board_state[j - 1][i - 1] == cell and board_state[j - 2][i - 2] == cell and board_state[j - 3][
                       i - 3] == cell:
                        return [(i - 1, j - 1), (i - 2, j - 2), (i - 3, j - 3), (i, j)]
                if i <= 2 and j <= 3:
                    if board_state[j + 1][i + 1] == cell and board_state[j + 2][i + 2] == cell and board_state[j + 3][
                       i + 3] == cell:
                        return [(i + 1, j + 1), (i + 2, j + 2), (i + 3, j + 3), (i, j)]
                if i >= 3 and j <= 3:
                    if board_state[j + 1][i - 1] == cell and board_state[j + 2][i - 2] == cell and board_state[j + 3][
                       i - 3] == cell:
                        return [(i - 1, j + 1), (i - 2, j + 2), (i - 3, j + 3), (i, j)]
                if i <= 2 and j >= 3:
                    if board_state[j - 1][i + 1] == cell and board_state[j - 2][i + 2] == cell and board_state[j - 3][
                       i + 3] == cell:
                        return [(i + 1, j - 1), (i + 2, j - 2), (i + 3, j - 3), (i, j)]
            i += 1
        j += 1
    return 0


def calculate(board_state, player, number_of_pieces):
    count = 0
    j = 0
    for col in board_state:
        i = 0
        for cell in col:
            if cell == player:
                if j == 3:
                    count += 1000
                try:
                    if i >= 4 - 1:
                        search_col = col[i - (4 - 1):i + 1]
                        count_dict = collections.Counter(search_col)
                        zeros_count = count_dict.get(0, 0)
                        cell_count = count_dict.get(cell, 0)
                        if cell_count == number_of_pieces and cell_count + zeros_count == 4:
                            count += 1
                    if i <= 6 - 4:
                        search_col = col[i:i + 4]

                        count_dict = collections.Counter(search_col)
                        zeros_count = count_dict.get(0, 0)
                        cell_count = count_dict.get(cell, 0)
                        if cell_count == number_of_pieces and cell_count + zeros_count == 4:
                            count += 1
                    if j >= 4 - 1:
                        search_col = board_state[j - (4 - 1):j + 1, i]
                        count_dict = collections.Counter(search_col)
                        zeros_count = count_dict.get(0, 0)
                        cell_count = count_dict.get(cell, 0)
                        if cell_count == number_of_pieces and cell_count + zeros_count == 4:
                            count += 1
                    if j <= 7 - 4:
                        search_col = board_state[j:j + 4, i]

                        count_dict = collections.Counter(search_col)
                        zeros_count = count_dict.get(0, 0)
                        cell_count = count_dict.get(cell, 0)
                        if cell_count == number_of_pieces and cell_count + zeros_count == 4:
                            count += 1

                    if i >= 3 and j >= 3:
                        cell_count = 0
                        zeros_count = 0
                        for change in range(3):
                            if board_state[j - change][i - change] == cell:
                                cell_count += 1
                            elif board_state[j - change][i - change] == 0:
                                zeros_count += 1
                        if cell_count == number_of_pieces and cell_count + zeros_count == 4:
                            count += 1
                    if i >= 3 and j <= 3:
                        cell_count = 0
                        zeros_count = 0
                        for change in range(3):
                            if board_state[j + change][i - change] == cell:
                                cell_count += 1
                            elif board_state[j + change][i - change] == 0:
                                zeros_count += 1
                        if cell_count == number_of_pieces and cell_count + zeros_count == 4:
                            count += 1
                    if i <= 2 and j >= 3:
                        cell_count = 0
                        zeros_count = 0
                        for change in range(3):
                            if board_state[j - change][i + change] == cell:
                                cell_count += 1
                            elif board_state[j - change][i + change] == 0:
                                zeros_count += 1
                        if cell_count == number_of_pieces and cell_count + zeros_count == 4:
                            count += 1
                    if i <= 2 and j <= 3:
                        cell_count = 0
                        zeros_count = 0
                        for change in range(3):
                            if board_state[j + change][i + change] == cell:
                                cell_count += 1
                            elif board_state[j + change][i + change] == 0:
                                zeros_count += 1
                        if cell_count == number_of_pieces and cell_count + zeros_count == 4:
                            count += 1
                except Exception as ve:
                    print(f"{i} -- {j}")
                    print(str(ve))
            i += 1
        j += 1
    return count


def get_heuristic(board_state, player):
    if player == 1:
        opponent = 2
    else:
        opponent = 1
    return 1000000 * calculate(board_state, player, 4) + 100 * calculate(board_state, player, 3) + 10 * calculate(
        board_state, player, 2) - 1000000 * calculate(board_state, opponent, 3)


def drop_piece(board_state, player, col_number):
    i = 0
    dropped = False
    for cell in board_state[col_number]:
        if cell == 0:
            board_state[col_number][i] = player
            dropped = True
            break
        i += 1
    if dropped:
        return True
    else:
        return False


def can_drop(board_state, col_number):
    i = 0
    for cell in board_state[col_number]:
        if cell == 0:
            return True
        i += 1
    return False


def valid_locations(board_state):
    col_numbers = []
    i = 0
    for _ in board_state:
        if can_drop(board_state, i):
            col_numbers.append(i)
        i += 1
    return col_numbers


AI_PLAYER = 2
USER = 1


def minimax(board_state, maximizing_player=True, alpha=-math.inf, beta=math.inf, depth=4, prune=True):
    player_win = check_win(board_state)
    if depth == 0 or player_win != 0 or (not np.any(board_state == 0)):
        if player_win != 0:
            if player_win == AI_PLAYER:
                return None, +math.inf
            elif player_win == USER:
                return None, -math.inf
        elif not np.any(board_state == 0):
            return None, 0
        else:
            return None, get_heuristic(board_state, AI_PLAYER)

    valid_locs = valid_locations(board_state)
    if maximizing_player:
        value = -math.inf
        col = valid_locs[0]
        for col_item in valid_locs:
            board_copy = board_state.copy()
            drop_piece(board_copy, AI_PLAYER, col_item)
            returned_col, recursive_score = minimax(board_copy, maximizing_player=False, alpha=alpha, beta=beta,
                                                    depth=depth - 1,
                                                    prune=prune)
            if recursive_score > value:
                value = recursive_score
                col = col_item
            alpha = max(value, alpha)
            if prune and alpha >= beta:
                break

        return col, value
    else:
        value = math.inf
        col = valid_locs[0]
        for col_item in valid_locs:
            board_copy = board_state.copy()
            drop_piece(board_copy, USER, col_item)
            returned_col, recursive_score = minimax(board_copy, maximizing_player=True, alpha=alpha, beta=beta,
                                                    depth=depth - 1,
                                                    prune=prune)
            if recursive_score < value:
                value = recursive_score
                col = col_item
            beta = min(value, beta)
            if prune and alpha >= beta:
                break
        return col, value
