# Problem 2: Valid Sudoku
from collections import Counter

def is_valid_sudoku(board):
    sudoku_counter = Counter()
    for row in range(9):
        for col in range(9):
            val = board[row][col]
            if val == ".":
                continue
            row_key = f"{val} in row {row}"
            col_key = f"{val} in col {col}"
            grid_key = f"{val} in {row // 3}-{col // 3}"
            
            sudoku_counter[row_key] += 1
            sudoku_counter[col_key] += 1
            sudoku_counter[grid_key] += 1
            
            if (sudoku_counter[row_key] > 1 or sudoku_counter[col_key] > 1 or sudoku_counter[grid_key] > 1): return False
    return True
    
board = [
["5","3",".",".","7",".",".",".","."],
["6",".",".","1","9","5",".",".","."],
[".","9","8",".",".",".",".","6","."],
["8",".",".",".","6",".",".",".","3"],
["4",".",".","8",".","3",".",".","1"],
["7",".",".",".","2",".",".",".","6"],
[".","6",".",".",".",".","2","8","."],
[".",".",".","4","1","9",".",".","5"],
[".",".",".",".","8",".",".","7","9"]
]

print(is_valid_sudoku(board))
    