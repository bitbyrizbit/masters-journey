class Solution:
    def islands(self, board):
        
        if not board:
            return 0
        
        ROWS, COLS = len(board), len(board)
        islands = 0
        
        def dfs(r, c):
            if r < 0 or c < 0 or r >= ROWS or c >= COLS or board[r][c] == "0":
                return
            board[r][c] = "0"
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == "1":
                    islands += 1
                    dfs(r, c)
        return islands

board_input = [
    ["1","1","1","1","0"],
    ["1","1","0","1","0"],
    ["1","1","0","0","0"],
    ["0","0","0","0","0"]
]
sol = Solution()
print(sol.islands(board_input))