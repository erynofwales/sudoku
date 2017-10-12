# Eryn Wells <eryn@erynwells.me>

from .. import SquareIsClue, ValueExistsInPeers, NoPossibleValues

class Backtrack(Exception):
    pass

def solve(sudoku):
    '''
    Implements a recursive backtracking Sudoku solver.
    '''
    return _solve_square(sudoku, 0, 0)

def _solve_square(sudoku, x, y):
    for value in sudoku.possible_values:
        try:
            print('({},{}) trying {}'.format(x, y, value))
            sudoku.set(x, y, value)
        except SquareIsClue:
            # Do nothing with this square; continue on to the next square below.
            print('({},{}) square is clue'.format(x,y))
            pass
        except ValueExistsInPeers:
            print('({},{}) value exists in peer set'.format(x,y))
            # Try next value.
            continue
        except NoPossibleValues:
            # Need to backtrack.
            print('({},{}) backtracking'.format(x,y))
            raise Backtrack()

        next_coord = _next_coord(sudoku, x, y)
        if not next_coord:
            break

        try:
            _solve_square(sudoku, *next_coord)
        except Backtrack:
            continue
    return sudoku

def _next_coord(sudoku, x, y):
    x += 1
    if x >= sudoku.row_size:
        (x, y) = (0, y + 1)
    if y >= sudoku.row_size:
        return None
    return (x, y)
