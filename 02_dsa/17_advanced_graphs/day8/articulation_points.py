def find_articulation_points(n, adj):
    dfn = [-1] * n
    low = [-1] * n
    is_ap = [False] * n
    timer = 0
    
    def dfs(u, p):
        nonlocal timer
        dfn[u] = low[u] = timer
        timer += 1
        children = 0
        
        for v in adj[u]:
            if v == p:
                continue
            if dfn[v] == -1:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if p != -1 and low[v] >= dfn[u]:
                    is_ap[u] = True
            else:
                low[u] = min(low[u], dfn[v])
                
        if p == -1 and children > 1:
            is_ap[u] = True
            
    for i in range(n):
        if dfn[i] == -1:
            dfs(i, -1)
            
    return [i for i in range(n) if is_ap[i]]
