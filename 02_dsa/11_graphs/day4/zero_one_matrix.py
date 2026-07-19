from collections import deque

class Solution:
    def matrix(self, mat):
        ROWS, COLS = len(mat), len(mat[0])
        queue = deque()
        
        for r in range(ROWS):
            for c in range(COLS):
                if mat[r][c] == 0:
                    queue.append((r, c))
                else:
                    mat[r][c] = -1
        
        while queue:
            r, c = queue.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and mat[nr][nc] == -1:
                    mat[nr][nc] = mat[r][c] + 1
                    queue.append((nr, nc))
        return mat

mat_input = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
sol = Solution()
print(sol.matrix(mat_input))
