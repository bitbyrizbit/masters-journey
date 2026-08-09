def is_scc(n, adj):
    def dfs(u, vis, g):
        vis[u] = True
        for v in g[u]:
            if not vis[v]:
                dfs(v, vis, g)
                
    vis = [False] * n
    dfs(0, vis, adj)
    if not all(vis):
        return False
        
    radj = [[] for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            radj[v].append(u)
            
    vis = [False] * n
    dfs(0, vis, radj)
    return all(vis)
