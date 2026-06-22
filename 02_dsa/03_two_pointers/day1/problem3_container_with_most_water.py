heights = [1,8,6,2,5,4,8,3,7]

def container(heights):
    left = 0 
    right = len(heights)-1
    max_area = 0
    while left < right:
        width = right - left
        height = min(heights[right],heights[left])
        area = width * height
        if area > max_area:
            max_area = area 
        if heights[left] < heights[right]:
            left += 1 
        else: 
            right -= 1
    return max_area
print(container(heights))