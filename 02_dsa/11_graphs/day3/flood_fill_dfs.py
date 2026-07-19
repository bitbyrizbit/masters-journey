class Solution:
    def flood_fill(self, image, sr, sc, color):
        starting_color = image[sr][sc]
        
        if starting_color == color:
            return image
        
        ROWS, COLS = len(image), len(image)
        
        def dfs(r, c):
            if r < 0 or c < 0 or r >= ROWS or c >= COLS or image[r][c] != starting_color:
                return
            image[r][c] = color
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        dfs(sr, sc)
        return image

image_input = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
sr_input = 1
sc_input = 1
color_input = 2
sol = Solution()
print(sol.flood_fill(image_input, sr_input, sc_input, color_input))