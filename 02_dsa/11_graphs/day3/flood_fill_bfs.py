from collections import deque

class Solution:
    def flood_fill(self, image, sr, sc, color):
        starting_color = image[sr][sc]
        
        if starting_color == color:
            return image
        
        ROWS, COLS = len(image), len(image)
        queue = deque([(sr, sc)])
        image[sr][sc] = color
        
        while queue:
            r, c = queue.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and image[nr][nc] == starting_color:
                    image[nr][nc] = color
                    queue.append((nr, nc))
        return image

image_input = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
sr_input = 1
sc_input = 1
color_input = 2
sol = Solution()
print(sol.flood_fill(image_input, sr_input, sc_input, color_input))