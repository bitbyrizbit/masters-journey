from collections import deque

class Solution:
    def oranges(self, grid):
        ROWS, COLS = len(grid), len(grid[0])
        queue = deque()
        fresh = 0
        time = 0
        
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1
        
        while queue and fresh > 0:
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))
            time += 1
        return time if fresh == 0 else -1

grid_input = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
sol = Solution()
print(sol.oranges(grid_input))