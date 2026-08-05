class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        if not intervals:
            return []
            
        # Sort intervals strictly by start coordinate
        intervals.sort(key=lambda x: x[0])
        
        merged = [intervals[0]]
        
        for i in range(1, len(intervals)):
            curr_start, curr_end = intervals[i]
            # If the current interval overlaps with the last merged interval
            if curr_start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], curr_end)
            else:
                merged.append(intervals[i])
                
        return merged

if __name__ == "__main__":
    sol = Solution()
    print(sol.merge([[1,3],[2,6],[8,10],[15,18]])) # Output: [[1,6],[8,10],[15,18]]
    print(sol.merge([[1,4],[4,5]]))                 # Output: [[1,5]]
