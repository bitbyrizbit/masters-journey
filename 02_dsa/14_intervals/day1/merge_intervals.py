class Solution:
    def merge(self, intervals):
        if not intervals:
            return []
            
        intervals.sort(key=lambda x: x[0])
        res = [intervals[0]]
        
        for i in range(1, len(intervals)):
            cur = intervals[i]
            prev = res[-1]
            
            if cur[0] <= prev[1]:
                prev[1] = max(prev[1], cur[1])
            else:
                res.append(cur)
                
        return res
