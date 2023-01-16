
def solve_sudoku(grid):
    """Find empty cell in grid
    :param grid: Required 9x9 Array
    """
    def find_empty():
        for row in range(9):
            for columnumn in range(9):
                if grid[row][columnumn] == 0:
                    return (row, columnumn)
        return None

    def is_valid(num, row, columnumn):
        """Check if number is a valid entry
        :param num: Number to check
        :param row: Rows of Matrix
        :param columnumn: columnumn of Matrix
        """
        # check row
        for x in range(9):
            if grid[row][x] == num:
                return False

        # check columnumn
        for x in range(9):
            if grid[x][columnumn] == num:
                return False

        # check 3x3 Square
        row2 = row - row % 3
        columnumn2 = columnumn - columnumn % 3
        for x in range(3):
            for y in range(3):
                if grid[x + row2][y+ columnumn2] == num:
                    return False
        return True

    def backtrack():
        """Backtracking"""
        empty = find_empty()
        if not empty:
            return True
        row, column = empty

        for num in range(1, 10):
            if is_valid(num, row, column):
                grid[row][column] = num
                if backtrack():
                    return True
                grid[row][column] = 0
        return False

    if backtrack():
        return grid
    else:
        return None

# Examples:
puzzle = [
            [0,0,0,1,0,4,0,0,0],
            [0,0,1,0,0,0,9,0,0],
            [0,9,0,7,0,3,0,6,0],
            [8,0,7,0,0,0,1,0,6],
            [0,0,0,0,0,0,0,0,0],
            [3,0,4,0,0,0,5,0,9],
            [0,5,0,4,0,2,0,3,0],
            [0,0,8,0,0,0,6,0,0],
            [0,0,0,8,0,6,0,0,0]
        ]
board = [
  [5, 3, 0, 0, 7, 0, 0, 0, 0],
  [6, 0, 0, 1, 9, 5, 0, 0, 0],
  [0, 9, 8, 0, 0, 0, 0, 6, 0],
  [8, 0, 0, 0, 6, 0, 0, 0, 3],
  [4, 0, 0, 8, 0, 3, 0, 0, 1],
  [7, 0, 0, 0, 2, 0, 0, 0, 6],
  [0, 6, 0, 0, 0, 0, 2, 8, 0],
  [0, 0, 0, 4, 1, 9, 0, 0, 5],
  [0, 0, 0, 0, 8, 0, 0, 7, 9]
  ]
#solve=solve_sudoku(puzzle)
#print(solve)