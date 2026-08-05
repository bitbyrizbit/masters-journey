class Solution:
    def eraseOverlapIntervals(self, intervals):
        if not intervals:
            return 0
            
        intervals.sort(key=lambda x: x[1])
        ans = 0
        end = float('-inf')
        
        for s, e in intervals:
            if s >= end:
                end = e
            else:
                ans += 1
                
        return ans
