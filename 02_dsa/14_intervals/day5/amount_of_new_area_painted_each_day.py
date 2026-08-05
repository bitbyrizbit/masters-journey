from typing import List

class Solution:
    def amountPainted(self, paint: List[List[int]]) -> List[int]:
        """
        Returns the amount of new area painted on each day.
        """
        # We use a jump array to skip over already painted regions in O(1) amortized time.
        # jumps[i] stores the next available unpainted coordinate if 'i' is already painted.
        # If jumps[i] == 0, coordinate 'i' is unpainted.
        
        if not paint:
            return []
            
        # Find the maximum coordinate to size our jump array
        max_coord = max(end for _, end in paint)
        jumps = [0] * (max_coord + 1)
        
        result = []
        
        for start, end in paint:
            work_done = 0
            curr = start
            
            while curr < end:
                if jumps[curr] == 0:
                    # Coordinate is unpainted! Paint it.
                    work_done += 1
                    # Update jump to point to the next coordinate
                    jumps[curr] = curr + 1
                    curr += 1
                else:
                    # Coordinate is already painted.
                    # We jump ahead to the next unpainted region.
                    next_jump = jumps[curr]
                    # Path Compression Optimization:
                    # Update the current jump to point to the END of this paint job,
                    # so future sweeps over this coordinate skip the entire block instantly.
                    jumps[curr] = max(jumps[curr], end)
                    curr = next_jump
                    
            result.append(work_done)
            
        return result
