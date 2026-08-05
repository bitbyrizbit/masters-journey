from typing import List

class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        """
        Returns the minimum number of arrows required to burst all balloons.
        """
        if not points:
            return 0
            
        # Sort by END coordinate
        points.sort(key=lambda x: x[1])
        
        arrows = 1
        current_arrow_pos = points[0][1]
        
        for i in range(1, len(points)):
            # If the balloon starts strictly after the current arrow position
            if points[i][0] > current_arrow_pos:
                # We need a new arrow. Shoot it at the end of this new balloon.
                arrows += 1
                current_arrow_pos = points[i][1]
                
        return arrows
