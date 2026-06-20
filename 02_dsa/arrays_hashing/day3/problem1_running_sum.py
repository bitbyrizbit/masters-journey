nums = [1,3,3,4]

def running_sum(nums):
    output_list = []
    for i in range(1,len(nums)+1):
        total = sum(nums[:i])
        output_list.append(total)
    return output_list
print(running_sum(nums))