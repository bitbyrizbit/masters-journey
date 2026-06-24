nums = [1,3,5,6]
target = 0

def search_insert(nums,target):
    low = 0 
    high = len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] < target:
            low = mid + 1
        elif nums[mid] > target: 
            high = mid - 1 
        else:    
            return mid
    return low

print(search_insert(nums,target))