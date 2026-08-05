# Definition for an Interval.
class Interval:
    def __init__(self, start: int = 0, end: int = 0):
        self.start = start
        self.end = end

class Solution:
    def employeeFreeTime(self, schedule: '[[Interval]]') -> '[Interval]':
        """
        Returns a list of finite intervals representing common, positive-length free time for all employees.
        """
        # Phase 1: Flatten all schedules into a single list
        intervals = []
        for emp in schedule:
            for iv in emp:
                intervals.append(iv)
                
        if not intervals:
            return []
            
        # Phase 2: Sort by start time
        intervals.sort(key=lambda x: x.start)
        
        free_time = []
        end = intervals[0].end
        
        # Phase 3: Coalesce Sweep to find gaps
        for i in range(1, len(intervals)):
            # If the next interval starts strictly after the maximum end time we've seen so far,
            # it means there is a complete gap across all employees!
            if intervals[i].start > end:
                free_time.append(Interval(end, intervals[i].start))
            
            # Always push the maximum end boundary forward
            end = max(end, intervals[i].end)
            
        return free_time
