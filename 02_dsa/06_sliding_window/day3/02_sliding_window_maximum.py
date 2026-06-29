nums = [1]
k = 1

def sliding_window_max(nums,k):
    if not nums or k > len(nums):
        return []
    start = 0
    end = 0
    output_list = [] 
    while end < len(nums): 
        if (end - start) + 1 < k:
            pass
        else: 
            current_max = max(nums[start:end + 1])     
            output_list.append(current_max)
            start += 1
        end += 1
    return output_list
print(sliding_window_max(nums,k))