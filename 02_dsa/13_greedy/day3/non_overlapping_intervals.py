class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        if not intervals:
            return 0
            
        # Sort intervals strictly by their end coordinate
        intervals.sort(key=lambda x: x[1])
        
        non_overlapping_count = 1
        curr_end = intervals[0][1]
        
        for i in range(1, len(intervals)):
            # If the next interval starts after or at the current end boundary, 
            # it is compatible and we can schedule it.
            if intervals[i][0] >= curr_end:
                non_overlapping_count += 1
                curr_end = intervals[i][1]
                
        # The number of intervals to remove is total intervals minus maximum non-overlapping intervals
        return len(intervals) - non_overlapping_count

if __name__ == "__main__":
    sol = Solution()
    print(sol.eraseOverlapIntervals([[1,2],[2,3],[3,4],[1,3]])) # Output: 1
    print(sol.eraseOverlapIntervals([[1,2],[1,2],[1,2]]))       # Output: 2
    print(sol.eraseOverlapIntervals([[1,2],[2,3]]))             # Output: 0
