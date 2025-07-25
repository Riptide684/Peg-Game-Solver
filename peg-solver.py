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

        return moves

    def on_board(self, square):
        if 0 <= square[0] < self.board_size and 0 <= square[1] < self.board_size:
            return self.board[square[0]][square[1]] != 2
        else:
            return 0

board = Board()
print(board.gen_moves())
