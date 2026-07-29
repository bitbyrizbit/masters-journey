import bisect

class Solution:
    def length_of_lis_dp(self, nums: list[int]) -> int:
        if not nums:
            return 0
        n = len(nums)
        dp = [1] * n
        
        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
                    
        return max(dp)

    def length_of_lis_patience(self, nums: list[int]) -> int:
        tails = []
        for num in nums:
            idx = bisect.bisect_left(tails, num)
            if idx == len(tails):
                tails.append(num)
            else:
                tails[idx] = num
        return len(tails)

nums_input = [10, 9, 2, 5, 3, 7, 101, 18]
sol = Solution()
print("O(N^2) DP Result:", sol.length_of_lis_dp(nums_input))         # Output: 4 (subsequence: [2, 3, 7, 101])
print("O(N log N) BS Result:", sol.length_of_lis_patience(nums_input)) # Output: 4
