from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Merges all overlapping intervals.
        """
        if not intervals:
            return []
            
        # Phase 1: Sort by start time.
        # This guarantees that if intervals overlap, they are adjacent in the list.
        intervals.sort(key=lambda x: x[0])
        
        # Phase 2: Sequential Coalesce.
        result = [intervals[0]]
        
        for i in range(1, len(intervals)):
            current = intervals[i]
            last_merged = result[-1]
            
            # If current interval starts at or before the previous interval ends, they overlap.
            if current[0] <= last_merged[1]:
                # The right boundary of the merged interval becomes the max of both end times.
                last_merged[1] = max(last_merged[1], current[1])
            else:
                # No overlap, commit the previous region and start tracking the new one.
                result.append(current)
                
        return result
