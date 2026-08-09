def kosaraju(n, adj):
    vis = [False] * n
    st = []
    
    def dfs1(u):
        vis[u] = True
        for v in adj[u]:
            if not vis[v]:
                dfs1(v)
        st.append(u)
        
    for i in range(n):
        if not vis[i]:
            dfs1(i)
            
    radj = [[] for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            radj[v].append(u)
            
    vis = [False] * n
    sccs = []
    
    def dfs2(u, comp):
        vis[u] = True
        comp.append(u)
        for v in radj[u]:
            if not vis[v]:
                dfs2(v, comp)
                
    while st:
        u = st.pop()
        if not vis[u]:
            comp = []
            dfs2(u, comp)
            sccs.append(comp)
            
    return sccs
