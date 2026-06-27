def binary_search_exact(nums, target):
    low = 0
    high = len(nums) - 1    
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1            
    return -1

def lower_bound(nums, target):
    low = 0
    high = len(nums) - 1
    result = len(nums)
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] >= target:
            result = mid
            high = mid - 1
        else:
            low = mid + 1     
    return result

def upper_bound(nums, target):
    low = 0
    high = len(nums) - 1
    result = len(nums)
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] > target:
            result = mid
            high = mid - 1
        else:
            low = mid + 1  
    return result

nums = [5,7,8,10]
print(binary_search_exact(nums, 8))
print(lower_bound(nums, 8))
print(upper_bound(nums, 8))