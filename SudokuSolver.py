def solve_sudoku(puzzle):
    # Find the next empty cell (represented by a 0) in the puzzle
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == 0:
                # Try filling the cell with a number from 1 to 9
                for k in range(1, 10):
                    # Check if the move is valid
                    if is_valid_move(puzzle, i, j, k):
                        # Make the move
                        puzzle[i][j] = k
                        # Recursively try to solve the puzzle
                        if solve_sudoku(puzzle):
                            return puzzle
                        # If the function returns False, reset the cell and try the next number
                        puzzle[i][j] = 0
                # If none of the numbers work, return False to the caller
                return False
    # If the function has iterated through all cells, the puzzle is solved
    return puzzle

def is_valid_move(puzzle, row, col, num):
    # Check if the number already exists in the same row
    for i in range(len(puzzle[0])):
        if puzzle[row][i] == num:
            return False
    # Check if the number already exists in the same column
    for i in range(len(puzzle)):
        if puzzle[i][col] == num:
            return False
    # Check if the number already exists in the same 3x3 subgrid
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if puzzle[start_row + i][start_col + j] == num:
                return False
    # If the number is not present in the same row, column, or subgrid, it is a valid move
    return True

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
  [0, 0, 0, 0, 8, 0, 0, 7,9]
  ]
#solve=solve_sudoku(puzzle)
#print(solve)