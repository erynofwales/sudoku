#!env python3
# Eryn Wells <eryn@erynwells.me>
'''
A Sudoku puzzle solver.
'''

import itertools
import math

class Sudoku:
    def __init__(self, size=9, initial=None):
        dim = math.sqrt(size)
        if dim != int(dim):
            raise ValueError('Board size must have an integral square root.')
        self._dimension = int(dim)
        self.size = size
        if initial:
            self.board = bytearray(initial)[:9**2]
        else:
            self.board = bytearray(b'\x00' * (size * size))

    @property
    def dimension(self):
        return self._dimension

    @property
    def rows(self):
        return self._apply_index_ranges(self.index_rows)

    @property
    def columns(self):
        return self._apply_index_ranges(self.index_columns)

    @property
    def squares(self):
        return self._apply_index_ranges(self.index_squares)

    @property
    def index_rows(self):
        '''
        Return an iterable of ranges of indexes into the board, each defining a row.
        '''
        sz = self.size
        return (range(i * sz, i * sz + sz) for i in range(sz))

    @property
    def index_columns(self):
        '''
        Return an iterable of ranges of indexes into the board, each defining a column.
        '''
        sz = self.size
        sz2 = sz ** 2
        return (range(i, sz2, sz) for i in range(sz))

    @property
    def index_squares(self):
        '''
        Return an iterable of ranges of indexes into the board, each defining a square.
        '''
        dim = self.dimension
        return (self.square(x, y) for y in range(dim) for x in range(dim))

    # TODO: Break the above into helper methods that produce a single thing given an index.

    @property
    def solved(self):
        expected = set(range(self.size))
        return all([
            all(expected == set(row) for row in self.rows),
            all(expected == set(col) for col in self.columns),
            all(expected == set(sqr) for sqr in self.squares)
        ])

    def square(self, x, y):
        dim = self.dimension
        if (x < 0 or x >= dim) or (y < 0 or y >= dim):
            raise IndexError('Invalid coordinates for square: ({}, {})'.format(x, y))

        offset = (x * dim, y * dim * self.size)

        def _range(i):
            start = (offset[1] + i * self.size) + offset[0]
            return range(start, start + dim)

        ranges = itertools.chain(*[_range(i) for i in range(dim)])
        return ranges

    def _apply_index_ranges(self, ranges):
        return ((self.board[i] for i in rng) for r in ranges)

    def __str__(self):
        field_width = len(str(self.size))
        dim = int(math.sqrt(self.size))
        lines = []
        spacer = '+' + '+'.join(['-' * (field_width * dim) for _ in range(dim)]) + '+'
        for line in range(self.size):
            chunks = []
            for i in range(dim):
                fields = []
                for j in range(dim):
                    idx = line * self.size + i * dim + j
                    fields.append('{{board[{i}]:^{width}}}'.format(i=idx, width=field_width))
                chunks.append(''.join(fields))
            if (line % dim) == 0:
                lines.append(spacer)
            lines.append('|' + '|'.join(chunks) + '|')
        lines.append(spacer)
        fmt = '\n'.join(lines)
        str_board = [str(n) if n != 0 else ' ' for n in self.board]
        out = fmt.format(board=str_board)
        return out
