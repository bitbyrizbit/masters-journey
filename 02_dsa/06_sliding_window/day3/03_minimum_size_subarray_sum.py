target = 1
nums = [1,4,4]

def min_size_subarray(nums,target):
    if not nums:
        return 0 
    left = 0
    current_sum = 0
    min_length = float('inf')
    for right in range(len(nums)):
        current_sum += nums[right]
        while current_sum >= target:
            min_length = min(min_length, right - left + 1)
            current_sum -= nums[left]
            left += 1
    return min_length if min_length != float('inf') else 0

print(min_size_subarray(nums,target))