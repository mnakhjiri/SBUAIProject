import random
import pickle
import numpy as np
from model.logic import check_win, can_drop, drop_piece, valid_locations, minimax


class SimpleGameBoard:
    def __init__(self, first_turn):
        self.empty_board = np.array([[0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0]])
        self.board_state = self.empty_board.copy()
        self.global_turn = first_turn
        self.player_win = 0

    def drop_piece(self, player, col_number):
        return drop_piece(self.board_state, player, col_number)

    def can_drop(self, col_number):
        return can_drop(board_state=self.board_state, col_number=col_number)

    def check_win(self):
        return check_win(self.board_state)

    def valid_locations(self):
        return valid_locations(self.board_state)


class Q:
    def __init__(self):
        self.cols = 7
        self.rows = 6
        self.num_actions = self.cols
        self.q_table = np.zeros((self.cols, self.rows, self.num_actions))
        self.epsilon = 0.2
        self.AIPlayer = 2
        self.epsilon = 0.2
        self.first_state_q_table = np.zeros(self.num_actions)

    def update_q_table(self, col, row, action, reward, next_state_col, next_state_row):
        learning_rate = 0.1
        discount_factor = 0.9
        self.q_table[col][row][action] += learning_rate * (
                reward + discount_factor * np.max(self.q_table[next_state_col][next_state_row]) -
                self.q_table[col][row][action])

    def update_q_table_first_state(self, action, reward, next_state_col, next_state_row):
        learning_rate = 0.1
        discount_factor = 0.9
        self.first_state_q_table[action] += learning_rate * (
                reward + discount_factor * np.max(self.q_table[next_state_col][next_state_row]) -
                self.first_state_q_table[action])

    def choose_action(self, col_state, row_state):
        if random.uniform(0, 1) < self.epsilon:
            action = random.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.q_table[col_state][row_state])
        return action

    def play_game(self):
        finished = False
        board = SimpleGameBoard(1)
        current_player = 1
        if random.uniform(0, 1) < self.epsilon:
            first_action = random.randint(0, self.num_actions - 1)
        else:
            first_action = np.argmax(self.first_state_q_table)
        board.drop_piece(current_player, first_action)
        row = 0
        for i in range(len(board.board_state[first_action])):
            if board.board_state[first_action][i] == 0:
                row = i - 1
                break
        self.update_q_table_first_state(first_action, 0, first_action, row)
        current_player = 2
        current_col = first_action
        current_row = row
        while not finished:
            if current_player == 2:
                action = self.choose_action(current_col, current_row)
                row = 0
                for i in range(len(board.board_state[action])):
                    if board.board_state[action][i] == 0:
                        row = i - 1
                        break
                if not board.drop_piece(current_player, action):
                    continue
                reward = 0
                if not np.any(board.board_state == 0):
                    finished = True
                    reward = 0
                elif board.check_win() == current_player:
                    finished = True
                    reward = 10
                self.update_q_table(current_col, current_row, action, reward, action, row)
                current_row = row
                current_col = action
                current_player = 1
            else:
                col, value = minimax(board.board_state, depth=2)
                row = 0
                for i in range(len(board.board_state[col])):
                    if board.board_state[col][i] == 0:
                        row = i - 1
                        break
                board.drop_piece(current_player, col)
                reward = 0
                if not np.any(board.board_state == 0):
                    finished = True
                    reward = 0
                if board.check_win() == current_player:
                    reward = -1
                    finished = True
                self.update_q_table(current_col, current_row, col, reward, col, row)
                current_row = row
                current_col = col
                current_player = 2


if __name__ == "__main__":
    num_episodes = 1
    q = Q()
    for episode in range(num_episodes):
        q.play_game()
        if episode % 10 == 0:
            print(episode)
    print(q.first_state_q_table)
    print(np.argmax(q.first_state_q_table))
    with open("q_table.pkl", "wb") as f:
        pickle.dump(q.q_table, f)
