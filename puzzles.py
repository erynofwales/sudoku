#!env python3
# Eryn Wells <eryn@erynwells.me>
'''
Parser for puzzles in the ./puzzles directory.
'''

import sudoku

euler = []
norvig = []

def parse_puzzle_files():
    global euler, norvig

    print('Parsing Euler puzzles')
    euler = list(_get_puzzles('puzzles/euler.txt'))

    print('Parsing Norvig puzzles')
    norvig = list(_get_puzzles('puzzles/norvig.txt'))

def _get_puzzles(filename):
    with open(filename, 'r') as f:
        puzzles = f.readlines()
    return (_parse_puzzle(p) for p in puzzles if p)

def _parse_puzzle(puzzle):
    puzzle = puzzle.strip()
    if len(puzzle) == 81:
        print("Parsing  '{}'".format(puzzle))
        board = (int('0' if x == '.' else x) for x in puzzle)
        return sudoku.Sudoku(initial=board)
    else:
        print("Skipping '{}'".format(puzzle))
        return None
