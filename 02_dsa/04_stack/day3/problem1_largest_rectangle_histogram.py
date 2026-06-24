def largest_rect(heights):
    stack = []
    max_area = 0
    heights = heights + [0] 
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height_idx = stack.pop()
            height = heights[height_idx]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)        
    return max_area

print(largest_rect([3, 3, 3, 3]))        
print(largest_rect([2, 1, 5, 6, 2, 3]))
