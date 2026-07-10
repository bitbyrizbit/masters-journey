class Solution:
    def sudoku(self, board):
        def is_valid(r, c, val):
            for i in range(9):
                if board[i][c] == val:
                    return False
                if board[r][i] == val:
                    return False
                if board[3 * (r // 3) + i // 3][3 * (c // 3) + i % 3] == val:
                    return False
            return True
        def solve():
            for r in range(9):
                for c in range(9):
                    if board[r][c] == ".":
                        for val in map(str, range(1, 10)):
                            if is_valid(r, c, val):
                                board[r][c] = val
                                if solve():
                                    return True
                                board[r][c] = "."
                        return False
            return True
        solve()

board_input = [
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
sol = Solution()
sol.sudoku(board_input)
print(board_input)