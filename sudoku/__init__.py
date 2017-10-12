#!env python3
# Eryn Wells <eryn@erynwells.me>
'''
A Sudoku puzzle solver.
'''

import itertools
import math

BOLD_SEQUENCE = '\x1B[1m'
UNBOLD_SEQUENCE = '\x1B[0m'

class Sudoku:
    def __init__(self, size=3, board=None):
        self._size = size
        sz4 = size ** 4
        if board:
            self._board = bytearray(board)[:sz4]
            self._clues = frozenset(i for i in range(len(self._board)) if self._board[i] != 0)
        else:
            self._board = bytearray(sz4)
            self._clues = frozenset()
        self._possible_values = None

    @property
    def size(self):
        '''
        The size of the board. This dictates the length of one side of the boxes that the board is subdivided into.
        '''
        return self._size

    @property
    def row_size(self):
        '''
        The length of a row or column, or the area of a box in the grid.
        '''
        return self.size ** 2

    @property
    def grid_size(self):
        '''
        The total number of squares in the grid.
        '''
        return self.size ** 4

    @property
    def all_squares(self):
        '''
        Iterator of xy-coordinates for every square in the grid.
        '''
        return itertools.product(range(self.row_size), repeat=2)

    @property
    def all_boxes(self):
        '''
        Iterator of xy-coordinates for every box in the grid.
        '''
        return itertools.product(range(self.size), repeat=2)

    @property
    def possible_values(self):
        '''
        The set of valid values for any grid square. This method does not account for values made invalid by already
        being present in a peer of a given square.
        '''
        if not self._possible_values:
            self._possible_values = set(range(1, self.row_size + 1))
        return self._possible_values

    @property
    def rows(self):
        return self._apply_index_ranges(self.index_rows)

    @property
    def columns(self):
        return self._apply_index_ranges(self.index_columns)

    @property
    def boxes(self):
        return self._apply_index_ranges(self.index_boxes)

    def peers(self, x, y):
        '''
        Return a set of values of the peers for a given square.
        '''
        return {self._board[i] for i in self.index_peers(x, y) if self._board[i] != 0}

    @property
    def index_rows(self):
        '''
        Return an iterable of ranges of indexes into the board, each defining a row.
        '''
        return (self._row(i) for i in range(self.row_size))

    @property
    def index_columns(self):
        '''
        Return an iterable of ranges of indexes into the board, each defining a column.
        '''
        return (self._column(i) for i in range(self.row_size))

    @property
    def index_boxes(self):
        '''
        Return an iterable of ranges of indexes into the board, each defining a box.
        '''
        return (self._box(x, y) for (x,y) in self.all_boxes)

    def index_peers(self, x, y):
        '''
        Return a set of the peers, indexes into the board, for a given square.
        '''
        idx = self._xy_to_idx(x, y)
        box = int(x / self.size), int(y / self.size)
        return (set(self._row(y)) | set(self._column(x)) | set(self._box(*box))) - {idx}

    def _row(self, r):
        row_size = self.row_size
        return range(r * row_size, r * row_size + row_size)

    def _column(self, c):
        return range(c, self.grid_size, self.row_size)

    def _box(self, x, y):
        size = self.size
        row_size = self.row_size
        offx, offy = (x * size, y * size * row_size)

        def _range(i):
            start = (offy + i * row_size) + offx
            return range(start, start + size)

        ranges = itertools.chain(*[_range(i) for i in range(size)])
        return ranges

    @property
    def solved(self):
        expected = self.possible_values
        all_groups = itertools.chain(self.rows, self.columns, self.boxes)
        return all(expected == set(g) for g in all_groups)

    def solve(self, solver):
        return solver(self)

    def set(self, x, y, value):
        if value not in self.possible_values:
            raise ValueError('{} not in set of possible values {}'.format(value, self.possible_values))

        peers = self.peers(x, y)
        if peers == self.possible_values:
            raise NoPossibleValues('Peer set for ({},{}) contains all possible values'.format(x, y))
        if value in peers:
            raise ValueExistsInPeers('{} already exists in the peer set for ({},{})'.format(value, x, y))

        self._set(x, y, value)

    def unset(self, x, y):
        self._set(x, y, 0)

    def _set(self, x, y, value):
        idx = self._xy_to_idx(x, y)
        if idx in self._clues:
            raise SquareIsClue('Cannot set clue square ({},{})'.format(x, y))
        self._board[idx] = value
        print('({},{}) <- {} {!r}'.format(x, y, value, self))

    def _xy_to_idx(self, x, y):
        return y * self.row_size + x

    def _apply_index_ranges(self, ranges):
        return ((self._board[i] for i in r) for r in ranges)

    def __repr__(self):
        return "{}(size={}, board='{}')".format(self.__class__.__name__,
                                                self.size,
                                                ''.join(str(i) for i in self._board))

    def __str__(self):
        field_width = len(str(max(self.possible_values)))
        spacer = '{0}{1}{0}'.format('+', '+'.join(['-' * (field_width * self.size) for _ in range(self.size)]))

        fmt = ''
        for (y,x) in self.all_squares:
            if x == 0:
                if y % self.size == 0:
                    if y != 0:
                        fmt += '\n'
                    fmt += '{spacer}'
                fmt += '\n'

            if x % self.size == 0:
                fmt += '|'

            idx = self._xy_to_idx(x,y)
            if idx in self._clues:
                bold = BOLD_SEQUENCE
                unbold = UNBOLD_SEQUENCE
            else:
                bold = unbold = ''
            fmt += '{bold}{{board[{i}]:^{{width}}}}{unbold}'.format(i=idx, bold=bold, unbold=unbold)

            if x == (self.row_size - 1):
                fmt += '|'
        fmt += '\n{spacer}'

        return fmt.format(board=[str(i) if i != 0 else ' ' for i in self._board], spacer=spacer, width=field_width)

class SudokuError(Exception):
    pass

class SquareIsClue(SudokuError):
    pass

class NoPossibleValues(SudokuError):
    pass

class ValueExistsInPeers(SudokuError):
    pass
