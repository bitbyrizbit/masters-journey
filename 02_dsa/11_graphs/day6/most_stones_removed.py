class Solution:
    def remove_stones(self, stones):
        parent = {}
        
        def find(x):
            if x not in parent:
                parent[x] = x
            if x != parent[x]:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x != root_y:
                parent[root_x] = root_y
        
        for r, c in stones:
            union(r, ~c)
        return len(stones) - len({find(x) for x in parent})

stones_input = [[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]
sol = Solution()
print(sol.remove_stones(stones_input))