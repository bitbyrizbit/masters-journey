def subarray_k_distinct(nums, k):
    def atMost(goal):
        if goal == 0:
            return 0
        counts = {}
        left = 0
        ans = 0
        for right in range(len(nums)):
            counts[nums[right]] = counts.get(nums[right], 0) + 1
            while len(counts) > goal:
                counts[nums[left]] -= 1
                if counts[nums[left]] == 0:
                    del counts[nums[left]]
                left += 1
            ans += right - left + 1
        return ans
    return atMost(k) - atMost(k - 1)

nums = [1,2,1,2,3]
k = 2
print(subarray_k_distinct(nums, k))
