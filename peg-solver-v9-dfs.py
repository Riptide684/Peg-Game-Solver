from time import time


class Game():
    def __init__(self, board_shape, board_size):
        self.board = 0
        self.board_mask = board_shape
        self.board_size = board_size
        self.l_column = self.get_l_column()
        self.r_column = self.get_r_column()
        self.h_masks = []
        self.v_masks = []
        self.h_tests_l = []
        self.h_tests_r = []
        self.v_tests_u = []
        self.v_tests_d = []
        self.v_magics = []
        self.d_magics = []
        self.v_shifts = []
        self.d_shifts = []
        self.precompute_masks()
        self.compute_magics()
        self.set_magics()

    def make_move(self, move):
        self.board ^= move

    def on_board(self, state):
        return state & self.board_mask == state
    
    def h_split(self, move):
        return (move & self.l_column != 0) and (move & self.r_column != 0)
    
    def get_l_column(self):
        l_column = 0
        for i in range(self.board_size):
            l_column += 2**(i*self.board_size)

        return l_column

    def get_r_column(self):
        r_column = 0
        for i in range(self.board_size):
            r_column += 2**((i+1)*self.board_size - 1)

        return r_column

    def precompute_masks(self):
        h_mask =            0b111
        v_mask =            1 + 2**self.board_size + 4**self.board_size
        h_test_l =          0b100
        h_test_r =          0b1
        v_test_u =          4**self.board_size
        v_test_d =          0b1

        for _ in range(self.board_size**2 - 2):
            if self.on_board(h_mask) and not self.h_split(h_mask):
                self.h_masks.append(h_mask)
                self.h_tests_l.append(h_test_l)
                self.h_tests_r.append(h_test_r)

            if self.on_board(v_mask):
                self.v_masks.append(v_mask)
                self.v_tests_u.append(v_test_u)
                self.v_tests_d.append(v_test_d)

            h_mask <<= 1
            h_test_l <<= 1
            h_test_r <<= 1

            v_mask <<= 1
            v_test_u <<= 1
            v_test_d <<= 1

    def compute_magics(self):
        mv = sum([2**i for i in range(self.board_size)])
        s = self.board_size * (self.board_size - 1)
        self.v_magics.append(mv)
        self.v_shifts.append(s)

        for _ in range((self.board_size // 2) - 1):
            mv <<= self.board_size
            s -= 2*self.board_size
            self.v_magics.append(mv)
            self.v_shifts.append(s)

        md = 1
        s = self.board_size**2 - 1
        self.d_magics.append(md)
        self.d_shifts.append(s)

        for i in range(self.board_size - 2):
            md <<= 1
            md += 2**(self.board_size*(i+1))
            s -= self.board_size + 1
            self.d_magics.append(md)
            self.d_shifts.append(s)

    def set_magics(self):
        func = ["def flip_vertical(b):"]

        for k in range(len(self.v_shifts)):
            func.append(f"    b = delta_swap(b, {self.v_magics[k]}, {self.v_shifts[k]})")

        func.append("    return b")

        exec("\n".join(func), globals())

        func = ["def flip_diag(b):"]

        for k in range(len(self.d_shifts)):
            func.append(f"    b = delta_swap(b, {self.d_magics[k]}, {self.d_shifts[k]})")
 
        func.append("    return b")

        exec("\n".join(func), globals())

    def gen_moves(self):
        moves = []
        
        b = self.board

        for i in range(len(self.h_masks)):
            h_mask = self.h_masks[i]
            v_mask = self.v_masks[i]
            h_test_l = self.h_tests_l[i]
            h_test_r = self.h_tests_r[i]
            v_test_u = self.v_tests_u[i]
            v_test_d = self.v_tests_d[i]

            if ((b ^ h_test_l) & h_mask == h_mask) or ((b ^ h_test_r) & h_mask == h_mask):
                moves.append(h_mask)

            if ((b ^ v_test_u) & v_mask == v_mask) or ((b ^ v_test_d) & v_mask == v_mask):
                moves.append(v_mask)

        return moves


class Solver():
    def __init__(self,  board_shape=0b0011100001110011111111111111111111100111000011100, 
                        board_start=0b0011100001110011111111110111111111100111000011100, board_size=7):
        self.states_to_explore = {board_start: []}
        self.game = Game(board_shape, board_size)
        self.game.board = board_start
        self.pegs = format(board_start, 'b').count('1') - 1

    def next_layer(self):
        layer = {}

        for board_state in self.states_to_explore:
            self.game.board = board_state
            prev = self.states_to_explore[self.game.board]
            moves = self.game.gen_moves()

            for move in moves:
                self.game.board = board_state
                self.game.make_move(move)

                symm_boards = get_symms(self.game.board)
                for b in symm_boards:
                    if b in layer:
                        break
                else:
                    layer[self.game.board] = prev + [move]

        return layer
    
    def display(self):
        for board in self.states_to_explore:
            display(board, self.game.board_size)

    def dfs(self, board, prev, searched, depth):
        if depth == self.pegs:
            print(prev)
            return 1
        
        self.game.board = board
        moves = self.game.gen_moves()

        for move in moves:
            self.game.board = board
            self.game.make_move(move)

            symm_boards = get_symms(self.game.board)
            for b in symm_boards:
                if b in searched[depth]:
                    break
            else:
                searched[depth].add(self.game.board)
                prev.append(move)
                res = self.dfs(self.game.board, prev, searched, depth+1)
                if res:
                    return 1
                prev.pop()

        global max_depth
        if depth > max_depth:
            max_depth = depth
            print(f"Max score: {depth}/{self.pegs}")

        return 0

    
    def solve(self):
        print('Starting solver...\n')
        self.dfs(self.game.board, [], [set() for _ in range(self.pegs)], 0)
        print('\nSolution found!')

    def perft(self):
        print('Starting performance test: \n')

        for i in range(self.pegs):
            start = time()
            self.states_to_explore = self.next_layer()
            end = time()
            time_taken = end - start
            print(str(len(self.states_to_explore)) + ' positions in layer ' + str(i+1))
            print('Exploring layer ' + str(i+1) + ' took ' + str(time_taken) + ' seconds\n')
            
        print('Performance test completed!')


def display(board, size):
    board = format(board, '0' + str(size**2) + 'b')
    rows = [board[size*i: size*(i+1)] for i in range(size)]
    print('\n'.join(rows))

def delta_swap(b, mask, delta):
   x = (b ^ (b >> delta)) & mask
   return   x ^ (x << delta)  ^ b

def rotate(b):
    return flip_vertical(flip_diag(b))

def get_symms(b):
    symms = [b]
    for i in range(3):
        b = rotate(b)
        symms.append(b)

    for j in range(4):
        symms.append(flip_vertical(symms[j]))

    return symms

def show_game(moves, shape, start, size):
    game = Game(shape, size)
    game.board = start
    display(game.board, size)
    print('')
    for move in moves:
        game.make_move(move)
        display(game.board, size)
        print('')


if __name__ == '__main__':
    max_depth = 0
    solver = Solver(0b000111000000111000000111000111111111111111111111111111000111000000111000000111000,
                    0b000111000000111000000111000111111111111101111111111111000111000000111000000111000, 9)

    solver.solve()
