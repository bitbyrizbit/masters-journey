nums = [2,1,5,1,3,2]
k = 3

def subarray(nums, k):
    if not nums or k > len(nums):
        return 0
    start = 0
    end = 0
    max_sum = 0 
    while end < len(nums): 
        if (end - start) + 1 < k:
            current_sum = sum(nums[start:end + 1])
            max_sum = max(current_sum, max_sum)
        else: 
            current_sum = sum(nums[start:end + 1])
            max_sum = max(current_sum, max_sum)     
            start += 1
        end += 1
    return max_sum

print(subarray(nums, k))
