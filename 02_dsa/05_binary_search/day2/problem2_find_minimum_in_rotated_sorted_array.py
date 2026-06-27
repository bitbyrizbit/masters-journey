def findMin(nums):
    if not nums:
        return -1
    low = 0
    high = len(nums) - 1
    while low < high:
        mid = (low + high) // 2
        if nums[mid] > nums[high]:
            low = mid + 1
        else:
            high = mid
    return nums[low]

nums = [3,4,5,1,2]
print(findMin(nums))