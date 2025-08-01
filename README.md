### Description ###
A solver for the peg solitaire game (https://en.wikipedia.org/wiki/Peg_solitaire). Works for any board shape that has D8 symmetry. 
Returns all possible final positions, and a single sequence of moves to arrive at them (unique up to rotation / reflection).

### How to use ###
Open v9, create an instance `solver` of `Solver`, and run `solver.Solver(args)`, where args specified the board shape, starting position, and board size in binary.
To view the output as a game, you can run show_game(moves, args).

To test performance, use `solver.perft()`. The version in C++ is fastest, but cannot yet do DFS.

### To do ###
- Allow the C++ to do DFS
