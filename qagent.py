import random
import copy
import json
import time

import logic

class Move():
    def __init__(self, key, result_board):
        self.key = key
        self.result_board = result_board

class QAgent():
    def __init__(self, learning_factor, refresh_factor, file_name):
        print('QAGENT INIT')
        self.filename = file_name

        try:
            with open(self.filename) as json_file:
                data_loaded = json.load(json_file)

            if len(data_loaded) == 0:
                data_loaded = {'games': 0, 'highest_score': 0, 'highest_tile': 0}

        except:
            data_loaded = {'games': 0, 'highest_score': 0, 'highest_tile': 0}

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
                    print('best curr qval = ')
                    print(current_qvalue)
                    current_best = available_pos[i]
            # else:
            #     undefined_found = True
            #     undefined_moves.append(available_pos[i])

        exploration_rate = 0.5

        # if undefined_found:
        #     print("UNDEFINED")
        #     random_value = random.randint(0, len(undefined_moves) - 1)
        #     chosen_move = undefined_moves[random_value]
        if current_best == None or random.uniform(0, 1) < exploration_rate:
            print("EXPLORATION")
            random_value = random.randint(0, len(available_pos) - 1)
            chosen_move = available_pos[random_value]
        else:
            print("------------------------------------BEST MOVE")
            chosen_move = current_best

        self.history.append(str(chosen_move.result_board))

        return chosen_move

    def receiveReward(self, reward, highest_tile):
        print('REVEIVED REWARD')
        try:
            values = self.data_loaded.values()
            # maxValue = 1
            maxValue = max(values)
        except:
            maxValue = reward

        self.data_loaded["games"] += 1
        if self.data_loaded["highest_score"] < reward:
            print('**************** NEW HIGHEST SCORE ****************' + str(reward))
            time.sleep(2)
            self.data_loaded["highest_score"] = reward
        if self.data_loaded["highest_tile"] < highest_tile:
            print('%%%%%%%%%%%%%% NEW HIGHEST TILE %%%%%%%%%%%%%%' + str(highest_tile))
            time.sleep(2)
            self.data_loaded["highest_tile"] = highest_tile
        for i in range(0, len(self.history)-1):
            tmp_value = 0
            if self.history[i] in self.data_loaded:
                tmp_value = copy.deepcopy(self.data_loaded[self.history[i]])
            self.data_loaded[self.history[i]] = tmp_value + (self.learning_factor * (reward + (self.refresh_factor * maxValue) - tmp_value))

        self.data_loaded[self.history[-1]] = reward

        with open(self.filename, 'w') as outfile:
            json.dump(self.data_loaded, outfile)

        self.history = []

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