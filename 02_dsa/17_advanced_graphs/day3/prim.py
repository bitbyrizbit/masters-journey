import heapq

class Solution:
    def minCostConnectPoints(self, points):
        n = len(points)
        vis = [False] * n
        h = [(0, 0)]
        ans = 0
        cnt = 0
        
        while cnt < n:
            d, u = heapq.heappop(h)
            if vis[u]:
                continue
            vis[u] = True
            ans += d
            cnt += 1
            
            for v in range(n):
                if not vis[v]:
                    dist = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                    heapq.heappush(h, (dist, v))
                    
        return ans
