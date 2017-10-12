#!env python3
# Eryn Wells <eryn@erynwells.me>
'''
Parser for puzzles in the ./puzzles directory.
'''

import argparse
import os.path
import sys

from sudoku import Sudoku, solvers

euler = []
norvig = []

def parse_puzzle_library(path, quiet=True):
    if not quiet:
        print('Parsing puzzles in {}'.format(path))
    puzzles = _get_puzzles(path, quiet)
    return puzzles

def _get_puzzles(filename, quiet):
    with open(filename, 'r') as f:
        puzzles = f.readlines()
    return (_parse_puzzle(p, quiet) for p in puzzles if p)

def _parse_puzzle(puzzle, quiet):
    puzzle = puzzle.strip()
    if len(puzzle) == 81:
        if not quiet:
            print("Parsing  '{}'".format(puzzle))
        board = (int('0' if x == '.' else x) for x in puzzle)
        return Sudoku(board=board)
    else:
        if not quiet:
            print("Skipping '{}'".format(puzzle))
        return None

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--solver', '-s', default=None,
                        help='The solver to use to solve this puzzle.')
    parser.add_argument('--verbose', '-v', action='store_true', default=False,
                        help='Print extra information when parsing puzzle libraries.')
    parser.add_argument('library',
                        help='A library file containing puzzles, one per line.')
    parser.add_argument('indexes', metavar='N', nargs='+', type=int,
                        help='0-based indexes of puzzles in the library')
    return parser.parse_args(args)

def main():
    args = parse_args(sys.argv[1:])
    puzzle_library = list(parse_puzzle_library(args.library, quiet=not args.verbose))
    for i in args.indexes:
        puzzle = puzzle_library[i]
        print(puzzle)
        if args.solver is not None:
            try:
                solver = getattr(solvers, args.solver)
                puzzle.solve(solver.solve)
            except AttributeError:
                print('No solver named {}'.format(args.solver))
            print(puzzle)
    return 0

if __name__ == '__main__':
    sys.exit(main())
