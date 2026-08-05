class Solution:
    def removeCoveredIntervals(self, intervals):
        intervals.sort(key=lambda x: (x[0], -x[1]))
        
        ans = 0
        mx = -1
        
        for s, e in intervals:
            if e > mx:
                ans += 1
                mx = e
                
        return ans
