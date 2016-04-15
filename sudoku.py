

class Sudoku(object):


    def __init__(self):
        self.grid = [[set(range(1, 10)) for i in range(9)] for j in range(9)]
        self.squares = [[set() for i in range(3)] for j in range(3)]
        self.rows = [set() for i in range(9)]
        self.columns = [set() for i in range(9)]
        self.locked = set()
        self.get_sudoku()

    def get_sudoku(self):
        print('Enter the gird row by row. Enter 0-9 with spaces for empty boxes')
        for row in range(9):
            raw_row = raw_input('row {}>> '.format(row+1))
            for i, n in enumerate(raw_row):
                if n == '\n':
                    break
                try:
                    n = int(n)
                    self.grid[row][i] = {n}
                    self.locked.add((row,i))
                except ValueError:
                    continue
        for row in range(9):
            for col in range(9):
                if (row, col) in self.locked:
                    n = next(iter(self.grid[row][col]))
                    print n, row, col
                    self.remove_potentials(
                        n,
                        row,
                        col,
                        self.square_from_coord(row, col)[0],
                    )

    def square_from_coord(self, row, col):
        square = 3 * (row / 3) + (col / 3)
        k = 3 * (row % 3) + (col % 3)
        return (square, k)

    def coord_from_square(self, square, k):
        row = 3 * (square / 3) + (k / 3)
        col = 3 * (square % 3) + (k % 3)
        return (row, col)

    def add_to_groups(self, n, row=None, col=None, square=None):
        if row:
            self.rows[row].add(n)
        if col:
            self.columns[col].add(n)
        if square:
            self.squares[square].add(n)


    def remove_potentials(self, n, row=None, col=None, square=None):
        self.add_to_groups(n, row, col, square)
        if row:
            for j in range(9):
                if (row, j) not in self.locked:
                    try:
                        self.grid[row][j].remove(n)
                    except KeyError:
                        continue
                    if len(self.grid[row][j]) == 1:
                        m = next(iter(self.grid[row][j]))
                        self.locked.add((row, j))
                        self.remove_potentials(
                            m,
                            row,
                            j,
                            self.square_from_coord(row, j)[0],
                        )
        if col:
            for i in range(9):
                if (i, col) not in self.locked:
                    try:
                        self.grid[i][col].remove(n)
                    except KeyError:
                        continue
                    if len(self.grid[i][col]) == 1:
                        m = next(iter(self.grid[i][col]))
                        self.locked.add((i, col))
                        self.remove_potentials(
                            m,
                            i,
                            col,
                            self.square_from_coord(i, col)[0],
                        )
        if square:
            for k in range(9):
                (i, j) = self.coord_from_square(square, k)
                if (i, j) not in self.locked:
                    try:
                        self.grid[i][j].remove(n)
                    except KeyError:
                        continue
                    if len(self.grid[i][j]) == 1:
                        m = next(iter(self.grid[i][j]))
                        self.locked.add((i, j))
                        self.remove_potentials(
                            m,
                            i,
                            j,
                            square,
                        )
