class Solution:
    def findCheapestPrice(self, n, flights, src, dst, k):
        dist = [float('inf')] * n
        dist[src] = 0
        
        for _ in range(k + 1):
            tmp = list(dist)
            for u, v, w in flights:
                if dist[u] != float('inf') and dist[u] + w < tmp[v]:
                    tmp[v] = dist[u] + w
            dist = tmp
            
        return dist[dst] if dist[dst] != float('inf') else -1
