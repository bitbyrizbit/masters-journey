import heapq
import collections

class Solution:
    def networkDelayTime(self, times, n, k):
        adj = collections.defaultdict(list)
        for u, v, w in times:
            adj[u].append((v, w))
            
        dist = {i: float('inf') for i in range(1, n + 1)}
        dist[k] = 0
        h = [(0, k)]
        
        while h:
            d, u = heapq.heappop(h)
            if d > dist[u]:
                continue
                
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(h, (dist[v], v))
                    
        mx = max(dist.values())
        return mx if mx != float('inf') else -1
