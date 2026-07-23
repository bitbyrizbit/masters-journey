class Solution:
    def delete_and_earn(self, nums: list[int]) -> int:
        if not nums:
            return 0
        
        max_val = max(nums)
        points = [0] * (max_val + 1)
        for num in nums:
            points[num] += num
        
        prev2 = 0  
        prev1 = 0  
        
        for p in points:
            curr = max(prev1, prev2 + p)
            prev2 = prev1
            prev1 = curr
            
        return prev1

nums_input = [3, 4, 2]
sol = Solution()
print(sol.delete_and_earn(nums_input))
