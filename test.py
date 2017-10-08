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
        self.assertEqual(len(self.board.board), 4**2)
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

class Sudoku4SolvedTests(Sudoku4TestCase):
    def test_that_an_empty_board_is_not_solved(self):
        self.assertFalse(self.board.solved)
