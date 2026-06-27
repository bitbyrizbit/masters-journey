def searchMatrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    rows = len(matrix)
    cols = len(matrix[0])
    left, right = 0, (rows * cols) - 1
    while left <= right:
        mid = (left + right) // 2
        mid_val = matrix[mid // cols][mid % cols]
        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    return False

print(searchMatrix([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 3))
print(searchMatrix([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 13))
print(searchMatrix([[1]], 1))
print(searchMatrix([[1,3]], 2))