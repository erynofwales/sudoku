#!/usr/bin/env python3
# Eryn Wells <eryn@erynwells.me>

'''
Tests for sudoku.
'''

import nose
import sudoku
import unittest


def test_9x9_dimensions():
    '''
    Test dimenions of a 9x9 Sudoku board.
    '''
    b = sudoku.Board()
    assert len(b.keys()) == 81
    assert b.size == 9
    assert b.box_size == 3
    for square, values in b.items():
        assert len(values) == 9


def test_9x9_units():
    '''
    Test units of a 9x9 Sudoku board.
    '''
    b = sudoku.Board()
    for r in range(b.size):
        row = b.row(r)
        assert len(row) == 9
        for sq in row:
            assert sq[1] == r

    for c in range(b.size):
        col = b.col(c)
        assert len(col) == 9
        for sq in col:
            assert sq[0] == c

    for x in range(0, b.size, b.box_size):
        for y in range(0, b.size, b.box_size):
            box = b.box(x, y)
            assert len(box) == 9
            # TODO: Finish this test

def test_9x9_row():
    '''
    A few tests on rows of a 9x9 Sudoku board.
    '''
    b = sudoku.Board()
    row = b.row(1)
    expected_keys = ((x, 1) for x in range(b.size))
    for ekey in expected_keys:
    	assert ekey in row
    # No negative numbers
    assert (-1, 1) not in row
    # Only squares with the right y-coordinate
    assert (0, 0) not in row
    # No keys above the size of the board
    assert (b.size, 1) not in row


def test_9x9_col():
    '''
    A few tests on rows of a 9x9 Sudoku board.
    '''
    b = sudoku.Board()
    col = b.col(3)
    expected_keys = ((3, y) for y in range(b.size))
    for ekey in expected_keys:
    	assert ekey in col
    # No negative numbers
    assert (3, -1) not in col
    # Only squares with the right x-coordinate
    assert (0, 0) not in col
    # No keys above the size of the board
    assert (3, b.size) not in col


def test_9x9_box():
    '''
    A few tests on boxes of a 9x9 Sudoku board.
    '''
    b = sudoku.Board()
    assert True


def test_9x9_peers():
    '''
    Test peers.
    '''
    b = sudoku.Board()
    peers = b.peers(3, 3)
    expected_peers = set(  [(x, 3) for x in range(b.size)]
                         + [(3, y) for y in range(b.size)]
                         + [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)])
    expected_peers.remove((3, 3))
    for epeer in expected_peers:
    	assert epeer in peers, '{} not in peers of (3, 3)'.format(epeer)


def test_9x9_str():
    '''
    Test string generation/printing.
    '''
    b = sudoku.Board()
    expected_str = '\n'.join(['. . . | . . . | . . .',
                              '. . . | . . . | . . .',
                              '. . . | . . . | . . .',
                              '------+-------+------',
                              '. . . | . . . | . . .',
                              '. . . | . . . | . . .',
                              '. . . | . . . | . . .',
                              '------+-------+------',
                              '. . . | . . . | . . .',
                              '. . . | . . . | . . .',
                              '. . . | . . . | . . .'])
    assert str(b) == expected_str


def main():
    nose.main()


if __name__ == '__main__':
    main()
