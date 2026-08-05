from typing import List

class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        """
        Returns True if a person could attend all meetings without conflicts.
        """
        # Sort by start time to line them up chronologically
        intervals.sort(key=lambda x: x[0])
        
        # Check every adjacent pair for overlaps
        for i in range(1, len(intervals)):
            # If the current meeting starts strictly before the previous one ends
            if intervals[i][0] < intervals[i - 1][1]:
                return False
                
        return True
