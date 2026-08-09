def tarjan(n, adj):
    dfn = [-1] * n
    low = [-1] * n
    vis = [False] * n
    st = []
    sccs = []
    timer = 0
    
    def dfs(u):
        nonlocal timer
        dfn[u] = low[u] = timer
        timer += 1
        st.append(u)
        vis[u] = True
        
        for v in adj[u]:
            if dfn[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif vis[v]:
                low[u] = min(low[u], dfn[v])
                
        if dfn[u] == low[u]:
            comp = []
            while True:
                v = st.pop()
                vis[v] = False
                comp.append(v)
                if v == u:
                    break
            sccs.append(comp)
            
    for i in range(n):
        if dfn[i] == -1:
            dfs(i)
            
    return sccs
