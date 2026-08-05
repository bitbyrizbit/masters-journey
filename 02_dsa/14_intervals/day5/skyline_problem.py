import heapq

class Solution:
    def getSkyline(self, buildings):
        events = []
        for l, r, h in buildings:
            events.append((l, -h, r))
            events.append((r, 0, 0))
            
        events.sort()
        
        h = [(0, float('inf'))]
        ans = []
        
        for x, neg_h, r in events:
            if neg_h != 0:
                heapq.heappush(h, (neg_h, r))
                
            while h[0][1] <= x:
                heapq.heappop(h)
                
            cur = -h[0][0]
            
            if not ans or ans[-1][1] != cur:
                ans.append([x, cur])
                
        return ans
