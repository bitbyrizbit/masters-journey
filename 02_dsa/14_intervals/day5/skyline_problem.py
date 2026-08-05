from typing import List
import heapq

class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        """
        Returns the key points of the skyline formed by a set of buildings.
        """
        # Step 1: Create discrete events for every building boundary.
        events = []
        for left, right, height in buildings:
            # We encode START events with a NEGATIVE height.
            # Why? If two events share the same X coordinate, sorting will process the larger negative height first!
            # This ensures we don't incorrectly drop the skyline to a smaller height or 0 at a vertical wall.
            events.append((left, -height, right))
            # END events have 0 height (they don't add to the skyline, they just trigger removals).
            events.append((right, 0, 0))
            
        # Sort events by X coordinate.
        events.sort()
        
        # Step 2: Max-Heap to track active buildings.
        # We store (-height, right_boundary). 
        # We seed it with a ground level (height 0) extending to infinity.
        active_heights = [(0, float('inf'))]
        result = []
        
        # Step 3: Process the Sweep-Line Events
        for x, neg_h, right in events:
            if neg_h != 0:
                # It's a START event. Push this building into the active heap.
                heapq.heappush(active_heights, (neg_h, right))
                
            # Crucial Cleanup Step: 
            # The building at the TOP of the max-heap might have already ended!
            # We lazily remove any expired buildings from the top of the heap.
            while active_heights[0][1] <= x:
                heapq.heappop(active_heights)
                
            # The current highest active building determines the skyline level
            current_max_height = -active_heights[0][0]
            
            # If this changes the previous skyline height, it's a key point!
            if not result or result[-1][1] != current_max_height:
                result.append([x, current_max_height])
                
        return result
