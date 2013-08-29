#!/usr/bin/env python3
# Eryn Wells <eryn@erynwells.me>

'''
A Sudoku solver.
'''

import logging
import math

LOG = logging.getLogger(__name__)


class Board(dict):
    def __init__(self, size=9, **kwargs):
        self.size = size

        # Verify size is a perfect square. The sqrt(size) is also the dimension of each box on the
        # Sudoku grid.
        self.box_size = int(math.sqrt(size))
        assert self.box_size == int(self.box_size), 'Invalid size; value must be a perfect square'

        # The range of possible values for a square.
        self.possible_values = range(1, self.size + 1)

        def kwget(x, y):
            '''
            Try to get an initial value for square ({x}, {y}) from the given kwargs. If none exists, return a list of
            all possible values for the square. If an initial value was given, make sure it is one of the valid initial
            values. Raise a ValueError if not.
            '''
            initial_value = kwargs.get('x{}y{}'.format(x, y))
            if initial_value is None:
                return list(self.possible_values)
            if initial_value not in self.possible_values:
                raise ValueError('Invalid initial value for square ({}, {}): {}'.format(x, y, initial_value))
            return [initial_value]

        # Make the grid.
        super(Board, self).__init__([(self._xy_key(x, y), kwget(x, y))
                                     for x in range(self.size)
                                     for y in range(self.size)])

    def _xy_key(self, x, y):
        '''Given {x} and {y}, generate a key to refer to the square at coordinate (x, y) in the grid.'''
        return (int(x), int(y))

    @property
    def solved(self):
        '''
        Determines if the board has been solved. First, determine if all squares have no more than one value (i.e. they
        have had values assigned to them). If not, return False. If so, check each unit (rows, columns, and boxes) to
        make sure that each has one and only one of each value in the range of possible values for a unit. If not,
        return False; otherwise, return True.
        '''
        if not all(len(s) == 1 for s in self.values()):
            return False

        def validate_unit(unit):
            '''
            Validate {unit} by ensuring it has exactly 1 of each value in the range of possible values.
            '''
            necessary_values = list(self.possible_values)
            for square, values in unit.items():
                v = values[0]
                if v in necessary_values:
                    necessary_values.remove(v)
                else:
                    return False
            if len(necessary_values) != 0:
                return False
            return True

        return (    all(validate_unit(self.row(r)) for r in range(self.size))
                and all(validate_unit(self.col(c)) for c in range(self.size))
                and all(validate_unit(self.box(x, y))
                        for x in range(0, self.size, self.box_size)
                        for y in range(0, self.size, self.box_size)))

    def row(self, idx):
        '''
        Return a dict of all squares in the {idx}'th row.
        '''
        assert idx >= 0 and idx < self.size, 'Invalid row index; value must be >= 0 and < {}'.format(self.size)
        # key[1] is Y coordinate in the grid.
        return {k: v for k, v in self.items() if k[1] == idx}

    def col(self, idx):
        '''
        Return a dict of all squares in the {idx}'th column.
        '''
        assert idx >= 0 and idx < self.size, 'Invalid column index; value must be >= 0 and < {}'.format(self.size)
        # key[0] is X coordinate in the grid.
        return {k: v for k, v in self.items() if k[0] == idx}

    def box(self, x, y):
        '''
        Given a square at coordinates ({x}, {y}), return a dictionary containing the squares that make up the box that
        contains the point.
        '''
        bx = int(x / self.box_size) * self.box_size
        by = int(y / self.box_size) * self.box_size
        bx_range = range(bx, bx + self.box_size)
        by_range = range(by, by + self.box_size)
        return {k: v for k, v in self.items() if k[0] in bx_range and k[1] in by_range}

    def peers(self, x, y):
        # Generate a dictionary of all the squares in the row, column, and box containing the given square.
        peers = dict(list(self.row(y).items()) + list(self.col(x).items()) + list(self.box(x, y).items()))
        # Remove the given square.
        del peers[self._xy_key(x, y)]
        return peers

    def clear(self):
        '''
        Clear the board.
        '''
        for square in self:
            self[square] = list(range(1, self.size + 1))

    def eliminate(self, square, value):
        '''
        Eliminate {value} from square at ({x}, {y}).
        '''
        if value not in self[square]:
            LOG.debug('Value {} not in square {}; skipping'.format(value, square))
            return

        # Update peer value list.
        super(Board, self).__setitem__(square, [v for v in self[square] if v != value])
        LOG.debug('Eliminating {} from square {}'.format(value, square))

        # (1) If a square is reduced to one value, eliminate that value from its peers.
        if len(self[square]) == 0:
            # Whoops. Removed the last value... We have a contradiction now.
            LOG.error('Removed last value from square {}'.format(square))
            raise ValueError('Removed last value from square {}; board is now invalid'.format(square))
        elif len(self[square]) == 1:
            # One value left in this square. Propagate changes to its peers.
            LOG.debug('One value left in square {}; eliminating {} from its peers'.format(square, self[square][0]))
            try:
                for peer in self.peers(*square):
                    self.eliminate(peer, self[square][0])
            except ValueError:
                raise

        # (2) If a unit has only one square for a value, put it there.
        for unit in (self.row(square[1]), self.col(square[0]), self.box(*square)):
            places = [sq for sq in unit if value in unit[sq]]
            if len(places) == 0:
                LOG.error('No place for value {} to go in unit {}'.format(value, unit))
                raise ValueError('No place for value {} to go in unit {}; board is now invalid'.format(value, unit))
            elif len(places) == 1:
                LOG.debug('One place for value {} to be in unit {}; setting'.format(value, unit))
                self[places[0]] = [value]
        return True

    def __delitem__(self, key):
        # Don't allow deleting keys from self.
        pass

    def __setitem__(self, key, value):
        #if key not in self:
            # Don't allow adding new keys, only changes to existing ones.
            #return
        LOG.debug('Setting value {} at {}.'.format(value, key))
        removed_values = set(self[key]) - set(value)
        for v in removed_values:
            self.eliminate(key, v)

    def __str__(self):
        lines = []
        box_lines = []
        for x in range(self.size):
            row_squares = []
            box_squares = []
            for y in range(self.size):
                square = self.get(self._xy_key(x, y))
                if len(square) == 1:
                    box_squares.append(str(square[0]))
                else:
                    box_squares.append('.')
                if len(box_squares) == self.box_size:
                    row_squares.append(' '.join(box_squares))
                    box_squares = []
            # Print a divider between boxes.
            box_lines.append(' | '.join(row_squares))
            if len(box_lines) == self.box_size:
                lines.append('\n'.join(box_lines))
                box_lines = []
                if x < self.size - 1:
                    box_dividers = ['-' * (2 * self.box_size - 1) for box in range(self.box_size)]
                    lines.append('\n{}\n'.format('-+-'.join(box_dividers)))
        return ''.join(lines)


