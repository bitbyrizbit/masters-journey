class Solution:
    def max_area_island(self, board):
        
        ROWS, COLS = len(board), len(board)
        max_area = 0
        
        def dfs(r, c):
            if r < 0 or c < 0 or r >= ROWS or c >= COLS or board[r][c] == 0:
                return 0
            board[r][c] = 0
            return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == 1:
                    max_area = max(max_area, dfs(r, c))
        return max_area

board_input = [
    [1,1,0,0,0],
    [1,1,0,0,0],
    [0,0,0,1,1],
    [0,0,0,1,1]
]
sol = Solution()
print(sol.max_area_island(board_input))