class Solution:
    def findMinArrowShots(self, points: list[list[int]]) -> int:
        if not points:
            return 0
            
        # Sort balloons strictly by their end coordinate
        points.sort(key=lambda x: x[1])
        
        arrows = 1
        curr_end = points[0][1]
        
        for i in range(1, len(points)):
            # If the next balloon starts AFTER the current arrow's end boundary, 
            # we need a new arrow.
            if points[i][0] > curr_end:
                arrows += 1
                curr_end = points[i][1]
                
        return arrows

if __name__ == "__main__":
    sol = Solution()
    print(sol.findMinArrowShots([[10,16],[2,8],[1,6],[7,12]])) # Output: 2
    print(sol.findMinArrowShots([[1,2],[3,4],[5,6],[7,8]]))    # Output: 4
    print(sol.findMinArrowShots([[1,2],[2,3],[3,4],[4,5]]))    # Output: 2
