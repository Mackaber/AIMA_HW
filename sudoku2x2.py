from csp import *

_R2 = list(range(2))
_CELL_C = itertools.count().__next__
_BGRID_C = [[[[_CELL_C() for x in _R2] for y in _R2] for bx in _R2] for by in _R2]
_ROWS_C = flatten([list(map(flatten, brow)) for brow in _BGRID_C])
#_BOXES_C  = flatten([list(map(flatten, zip(*brow))) for brow in _BGRID_C])
_COLS_C = list(zip(*_ROWS_C))

_NEIGHBORS_C = {v: set() for v in flatten(_ROWS_C)}
for unit in map(set, _ROWS_C + _COLS_C):
    for v in unit:
        _NEIGHBORS_C[v].update(unit - set([v]))

def summations_constraint(A, a, B, b):
    a = int(a)
    b = int(b)
    # return different_values_constraint(A, a, B, b)
    # A & B are the variables
    # a & b are the values
    if different_values_constraint(A, a, B, b):
        if (A == 0 and B == 4) or (A == 4 and B == 0):
            return a + b == 3

        if A == 1 and B == 5:
            return a + b == 7
        if A == 2 and B == 3:
            return a + b == 6
        if A == 6:
            return a == 1
        if B == 6:
            return b == 1
        if A == 7 and B == 11:
            return a + b == 4
        if A == 8 and B == 9:
            return a + b == 6
        if A == 12 and B == 13:
            return a + b == 4
        if A == 10 and B == 14:
            return a + b == 5
        if A == 15:
            return a == 4
        if B == 15:
            return b == 4
        else:
            return True
    else:
        return False

class Sudoku2x2(CSP):

    """A Sudoku problem.
    The box grid is a 3x3 array of boxes, each a 3x3 array of cells.
    Each cell holds a digit in 1..9. In each box, all digits are
    different; the same for each row and column as a 9x9 grid.
    >>> e = Sudoku(easy1)
    >>> e.display(e.infer_assignment())
    . . 3 | . 2 . | 6 . .
    9 . . | 3 . 5 | . . 1
    . . 1 | 8 . 6 | 4 . .
    ------+-------+------
    . . 8 | 1 . 2 | 9 . .
    7 . . | . . . | . . 8
    . . 6 | 7 . 8 | 2 . .
    ------+-------+------
    . . 2 | 6 . 9 | 5 . .
    8 . . | 2 . 3 | . . 9
    . . 5 | . 1 . | 3 . .
    >>> AC3(e); e.display(e.infer_assignment())
    True
    4 8 3 | 9 2 1 | 6 5 7
    9 6 7 | 3 4 5 | 8 2 1
    2 5 1 | 8 7 6 | 4 9 3
    ------+-------+------
    5 4 8 | 1 3 2 | 9 7 6
    7 2 9 | 5 6 4 | 1 3 8
    1 3 6 | 7 9 8 | 2 4 5
    ------+-------+------
    3 7 2 | 6 8 9 | 5 1 4
    8 1 4 | 2 5 3 | 7 6 9
    6 9 5 | 4 1 7 | 3 8 2
    >>> h = Sudoku(harder1)
    >>> backtracking_search(h, select_unassigned_variable=mrv, inference=forward_checking) is not None
    True
    """
    R3 = _R2
    Cell = _CELL_C
    bgrid = _BGRID_C
    #boxes = _BOXES_C
    rows = _ROWS_C
    cols = _COLS_C
    neighbors = _NEIGHBORS_C

    def __init__(self, grid):
        """Build a Sudoku problem from a string representing the grid:
        the digits 1-9 denote a filled cell, '.' or '0' an empty one;
        other characters are ignored."""
        squares = iter(re.findall(r'\d|\.', grid))
        domains = {var: [ch] if ch in '1234' else '1234'
                   for var, ch in zip(flatten(self.rows), squares)}
        for _ in squares:
            raise ValueError("Not a Sudoku grid", grid)  # Too many squares
        CSP.__init__(self, None, domains, self.neighbors, summations_constraint)

    def display(self, assignment):
        def show_box(box): return [' '.join(map(show_cell, row)) for row in box]

        def show_cell(cell): return str(assignment.get(cell, '.'))

        def abut(lines1, lines2): return list(
            map(' | '.join, list(zip(lines1, lines2))))
        print('\n----+----\n'.join(
            '\n'.join(reduce(
                abut, map(show_box, brow))) for brow in self.bgrid))

grid = '.1.2.41...3.4...'
e = Sudoku2x2(grid)
e.display(e.infer_assignment())
print()
#AC3(e); e.display(e.infer_assignment())
print()
grid = '......1........4'
s = Sudoku2x2(grid)
backtracking_search(s, select_unassigned_variable=mrv, inference=forward_checking)
s.display(s.infer_assignment())