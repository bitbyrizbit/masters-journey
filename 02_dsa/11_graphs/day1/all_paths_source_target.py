class Solution:
    def paths_source_target(self, graph):
        target = len(graph) - 1
        res = []
        path = []
        def dfs(node):
            path.append(node)
            if node == target:
                res.append(path.copy())
            else:
                for neighbor in graph[node]:
                    dfs(neighbor)
            path.pop()
        dfs(0)
        return res

graph_input = [[1,2],[3],[3],[]]
sol = Solution()
print(sol.paths_source_target(graph_input))