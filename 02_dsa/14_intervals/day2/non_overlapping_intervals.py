from typing import List

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        """
        Returns the minimum number of intervals to remove to make the rest non-overlapping.
        """
        if not intervals:
            return 0
            
        # Sort by END time (Earliest Finish Time First)
        intervals.sort(key=lambda x: x[1])
        
        removals = 0
        prev_end = float('-inf')
        
        for start, end in intervals:
            # If the current interval starts after or exactly when the previous one ends
            if start >= prev_end:
                # Keep it, and update the boundary
                prev_end = end
            else:
                # Overlap! We remove the current one (because the previous one ended earlier)
                removals += 1
                
        return removals
