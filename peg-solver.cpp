#include <vector>
#include <set>
#include <iostream>
#include <cstdint>
#include <chrono>

typedef uint64_t u64;


// def display(board):
//     board = format(board, '049b')
//     rows = [board[7*i: 7*(i+1)] for i in range(7)]
//     print('\n'.join(rows))

u64 delta_swap(u64 b, u64 mask, u64 delta) {
   u64 x = (b ^ (b >> delta)) & mask;
   return x ^ (x << delta)  ^ b;
}

u64 flip_vertical(u64 b) {
    b = delta_swap(b, 0b0000000000000000000000000000000000000000001111111, 42);
    b = delta_swap(b, 0b0000000000000000000000000000000000011111110000000, 28);
    b = delta_swap(b, 0b0000000000000000000000000000111111100000000000000, 14);
    return b;
}

u64 flip_diag(u64 b) {
    // flips along A1 G7 diagonal
    b = delta_swap(b, 1, 48);
    b = delta_swap(b, 0b0000000000000000000000000000000000000000010000010, 40);
    b = delta_swap(b, 0b0000000000000000000000000000000000100000100000100, 32);
    b = delta_swap(b, 0b0000000000000000000000000001000001000001000001000, 24);
    b = delta_swap(b, 0b0000000000000000000010000010000010000010000010000, 16);
    b = delta_swap(b, 0b0000000000000100000100000100000100000100000100000, 8);
    return b;
}

u64 rotate(u64 b) {
    return flip_vertical(flip_diag(b));
}

std::vector<u64> get_symms(u64 b) {
    std::vector<u64> symms(8);
    symms[0] = b;
    for (int i=1; i<4; i++) {
        b = rotate(b);
        symms[i] = b;
    }

    for (int j=0; j<4; j++) {
        symms[j+4] = flip_vertical(symms[j]);
    }

    return symms;
}


class Game {
    public:
    u64 board;

    Game() {
        board = 0b0011100001110011111111110111111111100111000011100;
    }

    void make_move(u64 move) {
        board ^= move;
    }

    std::vector<u64> gen_moves() {
        std::vector<u64> moves;

        const u64 h_masks[19] = {28, 3584, 114688, 229376, 458752, 917504, 1835008, 14680064, 29360128, 58720256, 117440512, 234881024, 
                    1879048192, 3758096384, 7516192768, 15032385536, 30064771072, 962072674304, 123145302310912};
        
        const u64 v_masks[19] = {66052, 132104, 264208, 8454656, 16909312, 33818624, 270548992, 541097984, 1082195968, 2164391936, 
                4328783872, 8657567744, 17315135488, 138521083904, 277042167808, 554084335616, 17730698739712, 
                35461397479424, 70922794958848};
        
        const u64 h_tests_l[19] = {16, 2048, 65536, 131072, 262144, 524288, 1048576, 8388608, 16777216, 33554432, 67108864, 134217728, 
                    1073741824, 2147483648, 4294967296, 8589934592, 17179869184, 549755813888, 70368744177664};
        
        const u64 h_tests_r[19] = {4, 512, 16384, 32768, 65536, 131072, 262144, 2097152, 4194304, 8388608, 16777216, 33554432, 
                    268435456, 536870912, 1073741824, 2147483648, 4294967296, 137438953472, 17592186044416};
        
        const u64 v_tests_u[19] = {65536, 131072, 262144, 8388608, 16777216, 33554432, 268435456, 536870912, 1073741824, 2147483648, 
                    4294967296, 8589934592, 17179869184, 137438953472, 274877906944, 549755813888, 17592186044416, 
                    35184372088832, 70368744177664};
        
        const u64 v_tests_d[19] = {4, 8, 16, 512, 1024, 2048, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 8388608, 16777216, 
                    33554432, 1073741824, 2147483648, 4294967296};

        for (int i=0; i<19; i++) {
            u64 h_mask = h_masks[i];
            u64 v_mask = v_masks[i];
            u64 h_test_l = h_tests_l[i];
            u64 h_test_r = h_tests_r[i];
            u64 v_test_u = v_tests_u[i];
            u64 v_test_d = v_tests_d[i];

            if ((((board ^ h_test_l) & h_mask) == h_mask) || (((board ^ h_test_r) & h_mask) == h_mask)) {
                moves.push_back(h_mask);
            }

            if ((((board ^ v_test_u) & v_mask) == v_mask) || (((board ^ v_test_d) & v_mask) == v_mask)) {
                moves.push_back(v_mask);
            }
        }

        return moves;
    }
};


class Solver {
    public:
    std::set<u64> states_to_explore;
    Game game;

    Solver() {
        states_to_explore.insert(0b0011100001110011111111110111111111100111000011100);
    }

    void next_layer() {
        std::set<u64> layer;

        for (u64 board_state : states_to_explore) {
            game.board = board_state;
            std::vector<u64> moves = game.gen_moves();

            for (u64 move : moves) {
                game.board = board_state;
                game.make_move(move);

                std::vector<u64> symm_boards = get_symms(game.board);
                bool found = false;
                for (u64 b : symm_boards) {
                    if (layer.count(b)) {
                        found = true;
                        break;
                    } 
                }
                if (!found) {
                    layer.insert(game.board);
                }
            }
        }

        states_to_explore = layer;
    }

    void perft() {
        std::cout << "Starting performance test: \n" << std::endl;

        for (int i=0; i<31; i++) {
            auto start = std::chrono::system_clock::now();
            next_layer();
            auto end = std::chrono::system_clock::now();
            auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
            std::cout << states_to_explore.size() << " positions in layer " << i+1 << "\n\n";
            std::cout << "Exploring layer " << i+1 << " took " << elapsed.count() << " ms\n" << std::endl;
        }
            
        std::cout << "Performance test completed!" << std::endl;
    }
};


int main() {
    Solver solver;
    solver.perft();
    return 0;
}
