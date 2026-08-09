import heapq

def dijkstra(n, adj, start):
    dist = [float('inf')] * n
    dist[start] = 0
    h = [(0, start)]
    
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue
            
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(h, (dist[v], v))
                
    return dist
