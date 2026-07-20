from collections import deque

class Solution:
    def safe_nodes(self, graph):
        n = len(graph)
        rev_adj = {i: [] for i in range(n)}
        indegree = [0] * n
        
        for src in range(n):
            for dest in graph[src]:
                rev_adj[dest].append(src)
                indegree[src] += 1
        
        queue = deque([i for i in range(n) if indegree[i] == 0])
        safe = [False] * n
        
        while queue:
            node = queue.popleft()
            safe[node] = True
            for neighbor in rev_adj[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
        return [i for i in range(n) if safe[i]]

graph_input = [[1, 2], [2, 3], [5], [0], [5], [], []]
sol = Solution()
print(sol.safe_nodes(graph_input))