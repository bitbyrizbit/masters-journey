class Solution:
    def criticalConnections(self, n, connections):
        adj = [[] for _ in range(n)]
        for u, v in connections:
            adj[u].append(v)
            adj[v].append(u)
            
        dfn = [-1] * n
        low = [-1] * n
        timer = 0
        ans = []
        
        def dfs(u, p):
            nonlocal timer
            dfn[u] = low[u] = timer
            timer += 1
            
            for v in adj[u]:
                if v == p:
                    continue
                if dfn[v] == -1:
                    dfs(v, u)
                    low[u] = min(low[u], low[v])
                    if low[v] > dfn[u]:
                        ans.append([u, v])
                else:
                    low[u] = min(low[u], dfn[v])
                    
        dfs(0, -1)
        return ans
