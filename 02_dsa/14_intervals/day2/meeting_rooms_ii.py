from typing import List
import heapq

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Returns the minimum number of conference rooms required.
        """
        if not intervals:
            return 0
            
        # Sort by start time so we process meetings in chronological order
        intervals.sort(key=lambda x: x[0])
        
        # Min-heap to track the END TIMES of active meetings
        heap = []
        
        for start, end in intervals:
            # If the earliest ending meeting finishes before or when this meeting starts
            if heap and heap[0] <= start:
                # Reuse the room! Update its end time.
                heapq.heapreplace(heap, end)
            else:
                # No room is free, open a new room
                heapq.heappush(heap, end)
                
        # The size of the heap is the peak number of rooms needed simultaneously
        return len(heap)
