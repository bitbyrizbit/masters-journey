def find_first_last(nums,target):
    start, end = -1, -1
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] >= target:
            high = mid - 1
        else:
            low = mid + 1
    if low < len(nums) and nums[low] == target:
        start = low
    else:
        return [-1, -1] 
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] <= target:
            low = mid + 1
        else:
            high = mid - 1
    end = high
    return [start, end] 

nums = [5,7,7,8,8,10]
target = 8
print(find_first_last(nums,target))