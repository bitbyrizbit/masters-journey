import heapq

class Solution:
    def minMeetingRooms(self, intervals):
        if not intervals:
            return 0
            
        intervals.sort(key=lambda x: x[0])
        h = []
        
        for s, e in intervals:
            if h and h[0] <= s:
                heapq.heapreplace(h, e)
            else:
                heapq.heappush(h, e)
                
        return len(h)
