# Eryn Wells <eryn@erynwells.me>

from collections import namedtuple
from enum import Enum
from .. import SquareIsClue, ValueExistsInPeers, NoPossibleValues

class Backtrack(Exception):
    pass

class ConstraintKind(Enum):
    CELL = 1
    ROW = 2
    COL = 3
    BOX = 4

Constraint = namedtuple('CellConstraint', ['kind', 'index', 'value'])
Possibility= namedtuple('Possibility', ['row', 'col', 'value'])

class Node:
    '''
    A doubly-linked list node that is a member of two distinct lists. One list is the row it is a member of. The other
    list is the column it is a member of.
    '''
    def __init__(self):
        # Horizontal linked list. West is "previous", east is "next".
        self.west = self.east = self
        # Vertical linked list. North is "previous", south is "next".
        self.north = self.south = self

    def insert_after_in_row(self, node):
        self._insert(node, 'west', 'east')

    def insert_before_in_col(self, node):
        self._insert(node, 'south', 'north')

    def iterate_row(self):
        return self._iterate('east')

    def iterate_col(self):
        return self._iterate('south')

    def _insert(self, node, prev_attr, next_attr):
        self_east = getattr(self, next_attr)    # Save my old next node
        setattr(self, next_attr, node)          # My next points to the new node
        setattr(node, next_attr, self_east)     # New node's next points to the old next
        setattr(node, prev_attr, self)          # New node's prev points to me
        if self_east:
            setattr(self_east, prev_attr, node) # Old next's prev points to the new node

    def _iterate(self, next_attr):
        cur = self
        while cur:
            yield cur
            cur = getattr(cur, next_attr)
            if cur == self:
                break

class Header(Node):
    '''
    A column header, including a count of the number of rows in this column.
    '''
    def __init__(self, constraint):
        Node.__init__(self)
        self.constraint = constraint
        self.number_of_rows = 0

    def append(self, node):
        self.insert_before_in_col(node)
        self.number_of_rows += 1
        node.header = self

class Cell(Node):
    '''
    A cell in the DLX matrix.
    '''
    def __init__(self, possibility):
        super(Cell, self).__init__()
        self.header = None
        self.possibility = possibility

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.possibility)

def solve(sudoku):
    '''
    Implements DLX, Don Knuth's Dancing Links version of Algorithm X, for solving exact cover problems.
    '''
    # TODO: Construct the matrix based on the provided sudoku.
    # TODO: Perform the algorithm on the matrix.
    # TODO: With the solution from running the algorithm above, fill in the sudoku.
    return sudoku

def _build_matrix(sudoku):
    # 1. Create headers for all columns.
    headers = _build_headers(sudoku)
    _build_rows(sudoku, headers)
    return headers

def _build_headers(sudoku):
    head = None
    cur = None

    def _insert_header(data):
        header = Header(data)
        if cur:
            cur.insert_after_in_row(header)
        return header

    # Cell constraints
    for i in range(sudoku.grid_size):
        cur = _insert_header(Constraint(ConstraintKind.CELL, i, None))

    # Row, Col, and Box constraints
    for kind in (ConstraintKind.ROW, ConstraintKind.COL, ConstraintKind.BOX):
        for i in range(sudoku.row_size):
            for value in sudoku.possible_values:
                cur = _insert_header(Constraint(kind, i, value))

    # Head points to the first column header
    head = cur.east

    return head

def _build_rows(sudoku, headers):
    for (index, coords) in enumerate(sudoku.all_squares):
        board_value = sudoku.get(*coords)
        possibilities = sudoku.possible_values_for_square(*coords)
        for value in possibilities:
            cur = None
            for col in headers.iterate_row():
                if col.constraint.index != index:
                    continue
                cell = Cell(Possibility(*coords, value))
                col.append(cell)
                if cur:
                    cur.insert_after_in_row(cell)
                cur = cell
