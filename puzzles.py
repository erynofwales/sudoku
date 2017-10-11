#!env python3
# Eryn Wells <eryn@erynwells.me>
'''
Parser for puzzles in the ./puzzles directory.
'''

import argparse
import sudoku
import sys

euler = []
norvig = []

def parse_puzzle_files(quiet=True):
    global euler, norvig

    if not quiet:
        print('Parsing Euler puzzles')
    euler.extend(_get_puzzles('puzzles/euler.txt', quiet))

    if not quiet:
        print('Parsing Norvig puzzles')
    norvig.extend(_get_puzzles('puzzles/norvig.txt', quiet))

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
        return sudoku.Sudoku(board=board)
    else:
        if not quiet:
            print("Skipping '{}'".format(puzzle))
        return None

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--euler', '-e', dest='library', action='store_const', const=euler, default=None)
    parser.add_argument('--norvig', '-n', dest='library', action='store_const', const=norvig, default=None)
    parser.add_argument('--verbose', '-v', action='store_true', default=False)
    parser.add_argument('indexes', metavar='N', nargs='+', type=int)
    return parser.parse_args(args)

def main():
    args = parse_args(sys.argv[1:])
    parse_puzzle_files(quiet=not args.verbose)
    for i in args.indexes:
        print(args.library[i])
    return 0

if __name__ == '__main__':
    sys.exit(main())
