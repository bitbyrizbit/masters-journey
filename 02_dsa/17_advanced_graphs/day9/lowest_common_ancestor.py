class TreeLCA:
    def __init__(self, n, edges, root=0):
        self.n = n
        self.log = 20
        self.depth = [0] * n
        self.up = [[0] * self.log for _ in range(n)]
        
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
            
        def dfs(u, p):
            self.up[u][0] = p
            for i in range(1, self.log):
                self.up[u][i] = self.up[self.up[u][i - 1]][i - 1]
            for v in adj[u]:
                if v != p:
                    self.depth[v] = self.depth[u] + 1
                    dfs(v, u)
                    
        dfs(root, root)
        
    def query(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
            
        diff = self.depth[u] - self.depth[v]
        for i in range(self.log):
            if (diff >> i) & 1:
                u = self.up[u][i]
                
        if u == v:
            return u
            
        for i in range(self.log - 1, -1, -1):
            if self.up[u][i] != self.up[v][i]:
                u = self.up[u][i]
                v = self.up[v][i]
                
        return self.up[u][0]
