def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    x, y = len(nums1), len(nums2)
    left, right = 0, x
    
    while left <= right:
        partitionX = (left + right) // 2
        partitionY = (x + y + 1) // 2 - partitionX
        maxLeftX = nums1[partitionX - 1] if partitionX > 0 else float('-inf')
        minRightX = nums1[partitionX] if partitionX < x else float('inf')
        maxLeftY = nums2[partitionY - 1] if partitionY > 0 else float('-inf')
        minRightY = nums2[partitionY] if partitionY < y else float('inf')
        if maxLeftX <= minRightY and maxLeftY <= minRightX:
            if (x + y) % 2 == 0:
                return (max(maxLeftX, maxLeftY) + min(minRightX, minRightY)) / 2.0
            else:
                return float(max(maxLeftX, maxLeftY))
        elif maxLeftX > minRightY:
            right = partitionX - 1
        else:
            left = partitionX + 1

print(findMedianSortedArrays([1, 3], [2]))
print(findMedianSortedArrays([1, 2], [3, 4]))
print(findMedianSortedArrays([0, 0], [0, 0]))
print(findMedianSortedArrays([], [1]))