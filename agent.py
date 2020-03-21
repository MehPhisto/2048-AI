import random
import copy
import json
import logic

class Move():
    def __init__(self, key, result_board):
        self.key = key
        self.result_board = result_board

class Agent():
    def __init__(self, learning_factor, refresh_factor, file_name):
        print('AGENT INIT')
        self.filename = file_name

        try:
            with open(self.filename) as json_file:
                data_loaded = json.load(json_file)

            if len(data_loaded) == 0:
                data_loaded = {'games': 0}

        except:
            data_loaded = {'games': 0}

        self.data_loaded = data_loaded

        self.learning_factor = learning_factor
        self.refresh_factor = refresh_factor
        self.history = []

        # self.learning_factor = 0.5 if self.learning_factor >= 1 or self.learning_factor <= 0 else print("potato")
        # self.refresh_factor = 0.5 if self.refresh_factor >= 1 or self.refresh_factor  <= 0 else print("potato")

    def play(self, board):
        available_pos = self.findAvailableMoves(board)
        current_qvalue = 0
        current_best = None
        undefined_found = False
        undefined_moves = []
        chosen_move = None

        for i in range(0, len(available_pos)):

            if str(available_pos[i].result_board) in self.data_loaded:
                if self.data_loaded[str(available_pos[i].result_board)] > current_qvalue:
                    current_qvalue = self.data_loaded[str(available_pos[i].result_board)]
                    current_best = available_pos[i]
            else:
                undefined_found = True
                undefined_moves.append(available_pos[i])

        if undefined_found:
            random_value = random.randint(0, len(undefined_moves) - 1)
            chosen_move = undefined_moves[random_value]
        elif current_best == None:
            random_value = random.randint(0, len(available_pos) - 1)
            chosen_move = available_pos[random_value]
        else:
            chosen_move = current_best

        self.history.append(str(chosen_move.result_board))

        return chosen_move

    def receiveReward(self, reward):
        print('REVEIVED REWARD')
        try:
            # values = self.data_loaded.values()
            maxValue = 1
            # maxValue = max(values)
        except:
            maxValue = reward

        self.data_loaded["games"] += 1
        for i in range(0, len(self.history)):
            if self.history[i] in self.data_loaded:
                tmp_value = copy.deepcopy(self.data_loaded[self.history[i]])
                self.data_loaded[self.history[i]] = \
                    tmp_value + \
                    self.learning_factor * (
                            reward + self.refresh_factor * maxValue - tmp_value)
            else:
                self.data_loaded[self.history[i]] = reward

        with open(self.filename, 'w') as outfile:
            json.dump(self.data_loaded, outfile)

    def findAvailableMoves(self, board):
        available_moves = []

        up_move = logic.up(board)
        if up_move[1] == True:
            available_moves.append(Move('z', up_move[0]))

        down_move = logic.down(board)
        if down_move[1] == True:
            available_moves.append(Move('s', down_move[0]))

        right_move = logic.right(board)
        if right_move[1] == True:
            available_moves.append(Move('d', right_move[0]))

        left_move = logic.left(board)
        if left_move[1] == True:
            available_moves.append(Move('q', left_move[0]))

        return available_moves