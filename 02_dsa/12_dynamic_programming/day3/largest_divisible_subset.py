class Solution:
    def largestDivisibleSubset(self, nums: list[int]) -> list[int]:
        if not nums:
            return []
            
        nums.sort()
        n = len(nums)
        dp = [1] * n
        parent = [-1] * n
        
        max_len = 1
        max_idx = 0
        
        for i in range(1, n):
            for j in range(i):
                if nums[i] % nums[j] == 0:
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        parent[i] = j
                        
            if dp[i] > max_len:
                max_len = dp[i]
                max_idx = i
                
        # Parent reconstruction
        result = []
        curr = max_idx
        while curr != -1:
            result.append(nums[curr])
            curr = parent[curr]
            
        return result[::-1]

nums_input = [1, 2, 4, 8]
sol = Solution()
print(sol.largestDivisibleSubset(nums_input))  # Output: [1, 2, 4, 8]
