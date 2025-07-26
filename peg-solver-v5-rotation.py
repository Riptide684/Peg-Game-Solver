import time


class Game():
    def __init__(self):
        self.board =        0b0011100001110011111111110111111111100111000011100
        self.board_mask =   0b0011100001110011111111111111111111100111000011100

    def make_move(self, move):
        # move looks like 0b01110
        self.board ^= move

    def on_board(self, state):
        return state & self.board_mask == state
    
    def h_split(self, h_mask):
        l_column =          0b1000000100000010000001000000100000010000001000000
        r_column =          0b0000001000000100000010000001000000100000010000001
        return (l_column & h_mask != 0) and (r_column & h_mask != 0)

    def gen_moves(self):
        # could just pre calculate all of the 3-masks
        h_mask =            0b0000000000000000000000000000000000000000000000111
        v_mask =            0b0000000000000000000000000000000000100000010000001
        h_test_l =          0b0000000000000000000000000000000000000000000000100
        h_test_r =          0b0000000000000000000000000000000000000000000000001
        v_test_u =          0b0000000000000000000000000000000000100000000000000
        v_test_d =          0b0000000000000000000000000000000000000000000000001

        moves = []

        # test for horizontal moves
        for _ in range(47):
            if self.on_board(h_mask) and not self.h_split(h_mask):
                if ((self.board ^ h_test_l) & h_mask == h_mask) or ((self.board ^ h_test_r) & h_mask == h_mask):
                    moves.append(h_mask)

            h_mask <<= 1
            h_test_l <<= 1
            h_test_r <<= 1

        # test for vertical moves (could combine)
        for _ in range(47):
            if self.on_board(v_mask):
                if ((self.board ^ v_test_u) & v_mask == v_mask) or ((self.board ^ v_test_d) & v_mask == v_mask):
                    moves.append(v_mask)

            v_mask <<= 1
            v_test_u <<= 1
            v_test_d <<= 1

        return moves


class Solver():
    def __init__(self):
        self.states_to_explore = [0b0011100001110011111111110111111111100111000011100]
        self.game = Game()

    def next_layer(self):
        layer = set()

        for board_state in self.states_to_explore:
            self.game.board = board_state
            moves = self.game.gen_moves()

            for move in moves:
                self.game.board = board_state
                self.game.make_move(move)

                symm_boards = get_symms(self.game.board)
                for b in symm_boards:
                    if b in layer:
                        break
                else:
                    layer.add(self.game.board)

        return layer
    
    def display(self):
        for board in self.states_to_explore:
            display(board.board)
            print('')
    
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
            print(str(len(self.states_to_explore)) + ' positions in layer ' + str(i+1))
            print('Exploring layer ' + str(i+1) + ' took ' + str(time_taken) + ' seconds\n')
            
        print('Performance test completed!')


def display(board):
    board = format(board, '049b')
    rows = [board[7*i: 7*(i+1)] for i in range(7)]
    print('\n'.join(rows))

def delta_swap(b, mask, delta):
   x = (b ^ (b >> delta)) & mask
   return   x ^ (x << delta)  ^ b

def flip_vertical(b):
    b = delta_swap(b, 0b0000000000000000000000000000000000000000001111111, 42)
    b = delta_swap(b, 0b0000000000000000000000000000000000011111110000000, 28)
    b = delta_swap(b, 0b0000000000000000000000000000111111100000000000000, 14)
    return b

def flip_diag(b):
    # flips along A1 G7 diagonal
    b = delta_swap(b, 1, 48)
    b = delta_swap(b, 0b0000000000000000000000000000000000000000010000010, 40)
    b = delta_swap(b, 0b0000000000000000000000000000000000100000100000100, 32)
    b = delta_swap(b, 0b0000000000000000000000000001000001000001000001000, 24)
    b = delta_swap(b, 0b0000000000000000000010000010000010000010000010000, 16)
    b = delta_swap(b, 0b0000000000000100000100000100000100000100000100000, 8)
    return b

def rotate(b):
    return flip_vertical(flip_diag(b))

def get_symms(b):
    symms = [b]
    for i in range(3):
        b = rotate(b)
        # could check if invariant here
        symms.append(b)

    for j in range(4):
        symms.append(flip_vertical(symms[j]))

    return symms

if __name__ == '__main__':
    solver = Solver()
    solver.perft()
