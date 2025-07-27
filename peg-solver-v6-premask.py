from time import time


class Game():
    def __init__(self):
        self.board =        0b0011100001110011111111110111111111100111000011100

    def make_move(self, move):
        # move looks like 0b01110
        self.board ^= move

    def gen_moves(self):
        moves = []

        h_masks = [28, 3584, 114688, 229376, 458752, 917504, 1835008, 14680064, 29360128, 58720256, 117440512, 234881024, 
                    1879048192, 3758096384, 7516192768, 15032385536, 30064771072, 962072674304, 123145302310912]
        
        v_masks = [66052, 132104, 264208, 8454656, 16909312, 33818624, 270548992, 541097984, 1082195968, 2164391936, 
                   4328783872, 8657567744, 17315135488, 138521083904, 277042167808, 554084335616, 17730698739712, 
                   35461397479424, 70922794958848]
        
        h_tests_l = [16, 2048, 65536, 131072, 262144, 524288, 1048576, 8388608, 16777216, 33554432, 67108864, 134217728, 
                     1073741824, 2147483648, 4294967296, 8589934592, 17179869184, 549755813888, 70368744177664]
        
        h_tests_r = [4, 512, 16384, 32768, 65536, 131072, 262144, 2097152, 4194304, 8388608, 16777216, 33554432, 
                     268435456, 536870912, 1073741824, 2147483648, 4294967296, 137438953472, 17592186044416]
        
        v_tests_u = [65536, 131072, 262144, 8388608, 16777216, 33554432, 268435456, 536870912, 1073741824, 2147483648, 
                     4294967296, 8589934592, 17179869184, 137438953472, 274877906944, 549755813888, 17592186044416, 
                     35184372088832, 70368744177664]
        
        v_tests_d = [4, 8, 16, 512, 1024, 2048, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 8388608, 16777216, 
                     33554432, 1073741824, 2147483648, 4294967296]

        for i in range(19):
            h_mask = h_masks[i]
            v_mask = v_masks[i]
            h_test_l = h_tests_l[i]
            h_test_r = h_tests_r[i]
            v_test_u = v_tests_u[i]
            v_test_d = v_tests_d[i]

            if ((self.board ^ h_test_l) & h_mask == h_mask) or ((self.board ^ h_test_r) & h_mask == h_mask):
                moves.append(h_mask)

            if ((self.board ^ v_test_u) & v_mask == v_mask) or ((self.board ^ v_test_d) & v_mask == v_mask):
                moves.append(v_mask)

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
            display(board)
            print('')
    
    def solve(self):
        print('Starting solver: \n')

        for i in range(31):
            print('Exploring layer ' + str(i+1))
            self.states_to_explore = self.next_layer()
            
        print('Found solution!')

    def perft(self):
        print('Starting performance test: \n')

        for i in range(31):
            start = time()
            self.states_to_explore = self.next_layer()
            end = time()
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
        symms.append(b)

    for j in range(4):
        symms.append(flip_vertical(symms[j]))

    return symms

if __name__ == '__main__':
    solver = Solver()
    solver.perft()
