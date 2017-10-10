#!env python3
# Eryn Wells <eryn@erynwells.me>
'''
Unit tests for the Sudoku module.
'''

import unittest
import sudoku

class Sudoku4TestCase(unittest.TestCase):
    def setUp(self):
        self.board = sudoku.Sudoku(size=4)

class Sudoku4BasicTests(Sudoku4TestCase):
    def test_that_board_is_sane(self):
        self.assertEqual(self.board.size, 4)
        self.assertEqual(len(self.board._board), 4**2)
        self.assertEqual(self.board.dimension, 2)

    def test_rows(self):
        expected_rows = [
            [ 0,  1,  2,  3],
            [ 4,  5,  6,  7],
            [ 8,  9, 10, 11],
            [12, 13, 14, 15]
        ]
        for (row, exrow) in zip(self.board.index_rows, expected_rows):
            row_list = list(row)
            with self.subTest(row=row_list, ex=exrow):
                self.assertEqual(row_list, exrow)

    def test_columns(self):
        expected_columns = [
            [0, 4,  8, 12],
            [1, 5,  9, 13],
            [2, 6, 10, 14],
            [3, 7, 11, 15]
        ]
        for (col, excol) in zip(self.board.index_columns, expected_columns):
            col_list = list(col)
            with self.subTest(col=col_list, ex=excol):
                self.assertEqual(col_list, excol)

    def test_squares(self):
        expected_squares = [
            [ 0,  1,  4,  5],
            [ 2,  3,  6,  7],
            [ 8,  9, 12, 13],
            [10, 11, 14, 15]
        ]
        for (sq, exsq) in zip(self.board.index_squares, expected_squares):
            sq_list = list(sq)
            with self.subTest(sq=sq_list, ex=exsq):
                self.assertEqual(sq_list, exsq)

    def test_peers(self):
        expected_peers = {
            (0,0): set([0, 1, 2, 3, 4, 8, 12, 5]),
            (1,0): set([0, 1, 2, 3, 5, 9, 13, 4]),
            (2,0): set([0, 1, 2, 3, 6, 10, 14, 7]),
            (3,0): set([0, 1, 2, 3, 7, 11, 15, 6]),

            (0,1): set([4, 5, 6, 7, 0, 8, 12, 1]),
            (1,1): set([4, 5, 6, 7, 1, 9, 13, 0]),
            (2,1): set([4, 5, 6, 7, 2, 10, 14, 3]),
            (3,1): set([4, 5, 6, 7, 3, 11, 15, 2]),

            (0,2): set([8, 9, 10, 11, 0, 4, 12, 13]),
            (1,2): set([8, 9, 10, 11, 1, 5, 13, 12]),
            (2,2): set([8, 9, 10, 11, 2, 6, 14, 15]),
            (3,2): set([8, 9, 10, 11, 3, 7, 15, 14]),

            (0,3): set([12, 13, 14, 15, 0, 4, 8, 9]),
            (1,3): set([12, 13, 14, 15, 1, 5, 9, 8]),
            (2,3): set([12, 13, 14, 15, 2, 6, 10, 11]),
            (3,3): set([12, 13, 14, 15, 3, 7, 11, 10]),
        }
        for (coords, expeers) in expected_peers.items():
            with self.subTest(coord=coords, ex=expeers):
                peers = self.board.index_peers(*coords)
                self.assertEqual(peers, expeers)

class Sudoku4SolvedTests(Sudoku4TestCase):
    def test_that_an_empty_board_is_not_solved(self):
        self.assertFalse(self.board.solved)
