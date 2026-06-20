import math
nums = [1,2,3,4]

def product_except_self(nums):
    output_list = []
    for i in range(0,len(nums)):
        product = math.prod(nums)
        current_prod = product // nums[i]
        output_list.append(current_prod)
    return output_list
print(product_except_self(nums))

def product_except_self(nums):
    output = [1] * len(nums)
    left_product = 1
    for i in range(len(nums)):
        output[i] = left_product
        left_product *= nums[i]
    right_product = 1
    for i in range(len(nums) - 1, -1, -1):
        output[i] *= right_product
        right_product *= nums[i]
    return output
nums = [1,2,3,4]
print(product_except_self(nums))
