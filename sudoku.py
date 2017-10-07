#!env python3
# Eryn Wells <eryn@erynwells.me>
'''
A Sudoku puzzle solver.
'''

import math

class Sudoku:
    def __init__(self, size=9):
        dim = math.sqrt(size)
        if dim != int(dim):
            raise ValueError('Board size must have an integral square root.')
        self.dimension = int(dim)
        self.size = size
        self.board = bytearray(b'\x00' * (size * size))

    @property
    def solved(self):
        def _check_group(group):
            values = sorted([self.board[i] for i in group])
            is_complete = values == list(range(1, self.size+1))
            return is_complete
        
        sz = self.size
        sz2 = sz ** 2
        dim = int(math.sqrt(self.size))

        rows = [range(i * sz, i * sz + sz) for i in range(sz)]
        cols = [range(i, sz2, sz) for i in range(sz)]
        # TODO: WIP

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
