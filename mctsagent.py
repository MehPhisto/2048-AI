import json
import math
import random
import sys
import logic

sys.setrecursionlimit(99999)

class Move():
    def __init__(self, key, result_board):
        self.key = key
        self.result_board = result_board


class MCTSAgent:
    def __init__(self, file_name):
        print('MCTSAgent INIT')
        self.filename = file_name

        try:
            with open(self.filename) as json_file:
                data_loaded = json.load(json_file)

            if len(data_loaded) == 0:
                data_loaded = {}

        except:
            data_loaded = {}

        self.data_loaded = data_loaded

        self.history = []
        self.sim_history = []

    def selection(self, board):
        print('SELECTION Loading........')
        board_hash = str(board)
        self.history.append(board_hash)
        if board_hash not in self.data_loaded:
            print('Expanding....')
            self.expansion(board)

        print('Simulating random moves....')
        # Run Random simu
        for i in range(100):
            print('Simulation number: ' + str(i))
            self.simulation(board)

        # FORMULA: (w/n)+c*sqrt(ln(N)/n)
        selection_data = {
            "max_value": 0,
            "key": ""
        }
        available_moves = self.findAvailableMoves(board)
        for move in available_moves:
            child_hash = logic.add_two(move["result_board"])
            if child_hash in self.data_loaded:
                w = self.data_loaded[child_hash]["tot_win"]
                n = self.data_loaded[child_hash]["tot_sim"]
                N = self.data_loaded[child_hash["parent_id"]]["tot_sim"]
            else:
                w = 0
                n = 0
                N = self.data_loaded[board_hash]
            c = math.sqrt(2)

            value = (w / n) + (c * math.sqrt(math.log(N) / n))
            if selection_data["max_value"] < value:
                selection_data["max_value"] = value
                selection_data["key"] = move["key"]

        return selection_data["key"]

    def expansion(self, board):
        board_hash = str(board)
        node_data = {
            "board": board_hash,
            "parent_id": 0 if len(self.history) == 0 else self.history[-1],
            "max_score": 0,
            "tot_win": 0,
            "tot_sim": 0,
            # "children_moves": []
        }

        # Generate possible moves + new tile generation
        # possible_children = [
        #     (logic.up(board)[0], logic.up(board)[1], 'z'),
        #     (logic.down(board)[0], logic.down(board)[1], 's'),
        #     (logic.right(board)[0], logic.right(board)[1], 'd'),
        #     (logic.left(board)[0], logic.left(board)[1], 'q'),
        # ]

        # for possible_child in possible_children:
        #     if possible_child[1] == True:
        #         node_data["children_moves"].append({
        #             # logic.add_two(board) is generating new tile
        #             "board": str(logic.add_two(possible_child[0])),
        #             "key": possible_child[2]
        #         })
        #         self.expansion(possible_child[0])

        self.data_loaded[board_hash] = node_data

    def simulation(self, board, i=0):
        if i == 0:
            self.sim_history = self.history
        else:
            self.sim_history.append(str(board))

        moves = self.findAvailableMoves(board)
        if len(moves) > 0:
            randIndex = random.randint(0, len(moves) - 1)
            chosen = moves[randIndex]
            self.simulation(chosen.result_board, i+1)
        else:
            max_tile = max(max(x) for x in board)
            self.backpropagation(logic.score(board), True if max_tile == 2048 else False)

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

    def backpropagation(self, score, win):
        for board_hash in self.sim_history:
            self.data_loaded[board_hash]["tot_sim"] += 1
            if win == True:
                self.data_loaded[board_hash]["tot_win"] += 1
            if self.data_loaded[board_hash]["max_score"] < score:
                self.data_loaded[board_hash]["max_score"] = score

        self.sim_history = []

        with open(self.filename, 'w') as outfile:
            json.dump(self.data_loaded, outfile)