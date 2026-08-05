class Solution:
    def missingNumber(self, nums):
        ans = len(nums)
        for i, x in enumerate(nums):
            ans ^= i ^ x
        return ans
