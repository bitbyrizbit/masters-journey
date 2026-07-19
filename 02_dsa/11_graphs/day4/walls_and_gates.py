from collections import deque

class Solution:
    def walls_and_gates(self, rooms):
        ROWS, COLS = len(rooms), len(rooms[0])
        queue = deque()
        
        for r in range(ROWS):
            for c in range(COLS):
                if rooms[r][c] == 0:
                    queue.append((r, c))
        
        while queue:
            r, c = queue.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and rooms[nr][nc] == 2147483647:
                    rooms[nr][nc] = rooms[r][c] + 1
                    queue.append((nr, nc))

rooms_input = [
    [2147483647, -1, 0, 2147483647],
    [2147483647, 2147483647, 2147483647, -1],
    [2147483647, -1, 2147483647, -1],
    [0, -1, 2147483647, 2147483647]
]
sol = Solution()
sol.walls_and_gates(rooms_input)
print(rooms_input)