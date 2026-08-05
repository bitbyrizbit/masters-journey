class Interval:
    def __init__(self, start=0, end=0):
        self.start = start
        self.end = end

class Solution:
    def employeeFreeTime(self, schedule):
        intervals = []
        for emp in schedule:
            for iv in emp:
                intervals.append(iv)
                
        if not intervals:
            return []
            
        intervals.sort(key=lambda x: x.start)
        ans = []
        end = intervals[0].end
        
        for i in range(1, len(intervals)):
            if intervals[i].start > end:
                ans.append(Interval(end, intervals[i].start))
            end = max(end, intervals[i].end)
            
        return ans
