class Solution:
    def valid_path(self, n, edges, source, destination):
        if source == destination:
            return True
        adj = {i: [] for i in range(n)}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        visit = set()
        
        def dfs(node):
            if node == destination:
                return True
            visit.add(node)
            for neighbor in adj[node]:
                if neighbor not in visit:
                    if dfs(neighbor):
                        return True
            return False
        return dfs(source)

n_input = 3
edges_input = [[0,1],[1,2],[2,0]]
source_input = 0
destination_input = 2
sol = Solution()
print(sol.valid_path(n_input, edges_input, source_input, destination_input))