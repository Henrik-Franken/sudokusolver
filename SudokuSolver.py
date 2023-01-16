
def solve_sudoku(grid):
    # function to find empty cell in grid
    def find_empty():
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return (row, col)
        return None

    # function to check if number is valid in current position
    def is_valid(num, row, col):
        # check row
        for i in range(9):
            if grid[row][i] == num:
                return False

        # check col
        for i in range(9):
            if grid[i][col] == num:
                return False

        # check 3x3 grid
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        return True

    # backtracking function
    def backtrack():
        empty = find_empty()
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if is_valid(num, row, col):
                grid[row][col] = num
                if backtrack():
                    return True
                grid[row][col] = 0
        return False

    if backtrack():
        return grid
    else:
        return None

# Example usage:
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