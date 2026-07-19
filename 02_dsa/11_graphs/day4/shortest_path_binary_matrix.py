from collections import deque

class Solution:
    def shortest_path(self, grid):
        N = len(grid)
        
        if grid[0][0] != 0 or grid[N-1][N-1] != 0:
            return -1
        
        queue = deque([(0, 0, 1)])
        grid[0][0] = 1
        
        while queue:
            r, c, length = queue.popleft()
            if r == N - 1 and c == N - 1:
                return length
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < N and 0 <= nc < N and grid[nr][nc] == 0:
                        grid[nr][nc] = 1
                        queue.append((nr, nc, length + 1))
        return -1

grid_input = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
sol = Solution()
print(sol.shortest_path(grid_input))