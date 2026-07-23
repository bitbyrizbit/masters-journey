class Solution:
    def max_alternating_sum(self, nums: list[int]) -> int:
        even = 0  
        odd = 0   
        
        for num in nums:
            next_even = max(even, odd + num)
            next_odd = max(odd, even - num)
            even, odd = next_even, next_odd
            
        return even

nums_input = [4, 2, 5, 3]
sol = Solution()
print(sol.max_alternating_sum(nums_input))  
