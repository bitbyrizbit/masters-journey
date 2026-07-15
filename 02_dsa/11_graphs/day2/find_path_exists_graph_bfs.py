from collections import deque

class Solution:
    def validPath(self, n: int, edges: list[list[int]], source: int, destination: int) -> bool:
        if source == destination:
            return True
        adj = {i: [] for i in range(n)}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        queue = deque([source])
        visit = {source}
        while queue:
            node = queue.popleft()
            if node == destination:
                return True
            for neighbor in adj[node]:
                if neighbor not in visit:
                    visit.add(neighbor)
                    queue.append(neighbor)
        return False

n_input = 3
edges_input = [[0, 1], [1, 2], [2, 0]]
source_input = 0
destination_input = 2
sol = Solution()
print(sol.validPath(n_input, edges_input, source_input, destination_input))
