nums = [-1,0,3,5,9,12]
target = 2

def binary_search(nums,target):
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
    return -1 
print(binary_search(nums,target))