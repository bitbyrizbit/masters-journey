class Solution:
    def island_perimeter(self, board):
        ROWS, COLS = len(board), len(board)
        perimeter = 0
        
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == 1:
                    perimeter += 4
                    if r > 0 and board[r-1][c] == 1:
                        perimeter -= 2
                    if c > 0 and board[r][c-1] == 1:
                        perimeter -= 2
        return perimeter

board_input = [[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]
sol = Solution()
print(sol.island_perimeter(board_input))