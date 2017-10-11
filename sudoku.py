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
            self._board = bytes(board)[:sz4]
            self._clues = set(i for i in range(len(self._board)) if self._board[i] != 0)
        else:
            self._board = bytes(sz4)
            self._clues = set()

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
        return set(range(1, self.row_size + 1))

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
        box = int(x / sz), int(y / sz)
        return set(self._row(y)) | set(self._column(x)) | set(self._box(*box))

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

    def _apply_index_ranges(self, ranges):
        return ((self._board[i] for i in r) for r in ranges)

    def __str__(self):
        field_width = len(str(max(self.possible_values)))
        sz = self.size
        lines = []
        spacer = '{0}{1}{0}'.format('+', '+'.join(['-' * (field_width * sz) for _ in range(sz)]))
        for line in range(self.row_size):
            chunks = []
            for i in range(sz):
                fields = []
                for j in range(sz):
                    idx = line * self.size + i * sz + j
                    if idx in self._clues:
                        bold = BOLD_SEQUENCE
                        unbold = UNBOLD_SEQUENCE
                    else:
                        bold = unbold = ''
                    fields.append('{bold}{{board[{i}]:^{{width}}}}{unbold}'.format(i=idx, bold=bold, unbold=unbold))
                chunks.append(''.join(fields))
            if (line % sz) == 0:
                lines.append(spacer)
            lines.append('{0}{1}{0}'.format('|', '|'.join(chunks)))
        lines.append(spacer)
        fmt = '\n'.join(lines)
        str_board = [str(n) if n != 0 else ' ' for n in self._board]
        out = fmt.format(board=str_board, width=field_width)
        return out
