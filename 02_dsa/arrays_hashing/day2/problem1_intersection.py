nums1 = [1,2,2,1]
nums2 = [2,2]

def intersection_brute(nums1,nums2):
    output_list = []
    for i in nums1:
        if i in nums2: 
            if i not in output_list:
                output_list.append(i)
    return output_list
print(intersection_brute(nums1,nums2))


def intersection_set(nums1,nums2):
    return list(set(nums1) & set(nums2))
print(intersection_set(nums1,nums2))