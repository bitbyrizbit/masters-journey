from typing import List

class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        """
        Returns the smallest sorted list of ranges that cover all the numbers in the array exactly.
        """
        if not nums:
            return []
            
        ranges = []
        start = nums[0]
        
        for i in range(1, len(nums)):
            # If the current number is not consecutive to the previous one, the range breaks.
            if nums[i] != nums[i - 1] + 1:
                # Format the completed range
                if start == nums[i - 1]:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}->{nums[i - 1]}")
                # Start tracking the new range
                start = nums[i]
                
        # Handle the final range after the loop finishes
        if start == nums[-1]:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}->{nums[-1]}")
            
        return ranges
