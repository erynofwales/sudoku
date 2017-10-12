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
    should_backtrack = False
    for value in sudoku.possible_values:
        should_backtrack = False
        try:
            sudoku.set(x, y, value)
        except SquareIsClue:
            # Do nothing with this square; continue on to the next square below.
            pass
        except ValueExistsInPeers:
            # Try next value.
            should_backtrack = True
            continue
        except NoPossibleValues:
            # Need to backtrack.
            sudoku.unset(x, y)
            raise Backtrack()

        next_coord = _next_coord(sudoku, x, y)
        if not next_coord:
            break

        try:
            return _solve_square(sudoku, *next_coord)
        except Backtrack:
            should_backtrack = True
            continue

    if should_backtrack:
        # Unhandled backtrack. Pop out of this one too.
        try:
            sudoku.unset(x, y)
        except SquareIsClue:
            pass
        raise Backtrack()

    return sudoku

def _next_coord(sudoku, x, y):
    x += 1
    if x >= sudoku.row_size:
        (x, y) = (0, y + 1)
    if y >= sudoku.row_size:
        return None
    return (x, y)
