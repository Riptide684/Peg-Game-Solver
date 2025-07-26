import copy
import time


class Board():
    def __init__(self):
        # 0 empty, 1 peg, 2 off board
        self.board = [
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2],
        ]

        self.board_size = len(self.board[0])

    def make_move(self, start, end):
        # coords like: start = [0, 2]
        self.board[start[0]][start[1]] = 0
        self.board[end[0]][end[1]] = 1
        middle = [(start[0] + end[0])//2, (start[1] + end[1])//2]
        self.board[middle[0]][middle[1]] = 0

    def gen_moves(self):
        # returns all possible moves
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        moves = []

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] != 1:
                    continue
                    
                for d in directions:
                    middle = [i + d[0], j + d[1]]
                    end = [i + 2*d[0], j + 2*d[1]]
                    if self.on_board([middle[0], middle[1]]) and self.board[middle[0]][middle[1]] == 1:
                        if self.on_board([end[0], end[1]]) and self.board[end[0]][end[1]] == 0:
                            moves.append([[i, j], end])

        # could improve by just looking for 110 pattern

        return moves

    def on_board(self, square):
        if 0 <= square[0] < self.board_size and 0 <= square[1] < self.board_size:
            return self.board[square[0]][square[1]] != 2
        else:
            return 0
        
    def display(self):
        text = ""
        symbols = [' ', 'O', ' ']
        for i in range(self.board_size):
            for j in range(self.board_size):
                text = text + str(symbols[self.board[i][j]])
            
            text = text + "\n"

        print(text[:-1])


class Solver():
    def __init__(self):
        self.states_to_explore = [Board()]

    def next_layer(self):
        # for now state is a Board object
        layer = []

        for state in self.states_to_explore:
            moves = state.gen_moves()
            # transposition table? (+rotation/reflection)
            for move in moves:
                new_board = Board()
                new_board.board = copy.deepcopy(state.board)
                # bad for memory and speed
                new_board.make_move(move[0], move[1])
                layer.append(new_board)

        return layer
    
    def display(self):
        for board in self.states_to_explore:
            board.display()
            print('\n')
    
    def solve(self):
        print('Starting solver: \n')
        # could do meet in the middle
        for i in range(31):
            print('Exploring layer ' + str(i+1))
            self.states_to_explore = self.next_layer()
            
        print('Found solution!')

    def perft(self):
        print('Starting performance test: \n')

        for i in range(31):
            start = time.time()
            self.states_to_explore = self.next_layer()
            end = time.time()
            time_taken = end - start
            print(str(len(self.states_to_explore)) + ' positions (w/ transpo) in layer ' + str(i+1))
            print('Exploring layer ' + str(i+1) + ' took ' + str(time_taken) + ' seconds\n')
            
        print('Performance test completed!')


if __name__ == '__main__':
    solver = Solver()
    solver.perft()
