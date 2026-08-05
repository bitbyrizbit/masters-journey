from typing import List

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        """
        Inserts a new interval into a sorted list of non-overlapping intervals,
        merging if necessary.
        """
        result = []
        i = 0
        n = len(intervals)
        
        # Phase 1: Collect all intervals completely BEFORE the new interval.
        # (Their end time is strictly less than the new interval's start time).
        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1
            
        # Phase 2: Merge all OVERLAPPING intervals.
        # (An interval overlaps if its start is less than or equal to new interval's end).
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
            
        # Add the fully merged new interval.
        result.append(newInterval)
        
        # Phase 3: Collect all intervals completely AFTER the new interval.
        while i < n:
            result.append(intervals[i])
            i += 1
            
        return result
