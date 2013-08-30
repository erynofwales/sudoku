#!/usr/bin/env python3
# Eryn Wells <eryn@erynwells.me>

'''
Parser for puzzles in the ./puzzles directory.
'''

import sudoku


euler = []
norvig = []


def parse_euler(filename='./puzzles/euler.txt'):
    with open(filename, 'r') as f:
        puzzle_lines = f.readlines()

    for puzzle in puzzle_lines:
        # Chop the newline
        if puzzle[-1] == '\n':
            puzzle = puzzle[:-1]
        print('Parsing puzzle: {}'.format(puzzle))
        if len(puzzle) != 81:
            continue
        kwargs = {}
        for idx in range(len(puzzle)):
            sq = puzzle[idx]
            if sq not in '1234567890.':
                continue
            sq_int = 0 if sq == '.' else int(sq)
            x, y = int(idx % 9), int(idx / 9)
            if sq_int != 0:
                kwargs[sudoku.Board.xy_kwargs_key(x, y)] = sq_int
        euler.append(sudoku.Board(**kwargs))


def parse_norvig(filename='./puzzles/norvig.txt'):
    with open(filename, 'r') as f:
        puzzle_lines = f.readlines()

    for puzzle in puzzle_lines:
        # Chop the newline
        if puzzle[-1] == '\n':
            puzzle = puzzle[:-1]
        print('Parsing puzzle: {}'.format(puzzle))
        if len(puzzle) != 81:
            continue
        kwargs = {}
        for idx in range(len(puzzle)):
            sq = puzzle[idx]
            if sq not in '1234567890.':
                continue
            sq_int = 0 if sq == '.' else int(sq)
            x, y = int(idx % 9), int(idx / 9)
            if sq_int != 0:
                kwargs[sudoku.Board.xy_kwargs_key(x, y)] = sq_int
        norvig.append(sudoku.Board(**kwargs))
