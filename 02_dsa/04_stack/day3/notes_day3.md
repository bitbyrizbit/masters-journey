## Problem: Largest Rectangle in Histogram

* Brute force: Evaluating every possible pair of bars as left and right boundaries using nested loops, finding the minimum height within that range, and calculating all potential rectangle areas.
```python
def largest_rectangle_brute(heights):
    max_area = 0
    n = len(heights)
    for i in range(n):
        min_height = heights[i]
        for j in range(i, n):
            min_height = min(min_height, heights[j])
            width = j - i + 1
            max_area = max(max_area, min_height * width)
    return max_area
```
* Optimized: Maintaining a monotonic increasing stack of indices and appending a sentinel `0` value to the end of the list to force a complete stack flush, calculating rectangle areas instantly whenever a shorter bar determines the right boundary for previous heights.
```python
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
```
* Data structure used: Nested loops for brute force; A sequential index tracking list operating as a monotonic increasing Stack (`list`) for optimization.
* Complexity:
  * Brute Force: Time O(n²) due to looking ahead across all remaining index configurations; Space O(1) constant memory.
  * Optimized: Time O(n) because every individual bar index is pushed onto and popped from the stack exactly once; Space O(n) to buffer uncollapsed indices.
* Mistakes made: Attempting to solve the problem by sorting the heights list first. This completely destroyed the spatial adjacency requirement of the histogram bars and rendered coordinate width calculations impossible. Furthermore, trying to track expansions using a basic scalar loop counter failed because a flat incrementer cannot capture the non-linear width boundaries triggered when heights drop significantly.
* What I learned: The monotonic increasing stack helps find the nearest smaller element on the left and right for every bar. Those boundaries determine the maximum width over which that bar can act as the limiting height. Appending a dummy `0` height at the end acts as a sentinel trigger, ensuring all remaining bars in the stack are flushed and their areas computed before returning.

---

## Problem: Binary Search

* Brute force: Linear scan through the array from index 0 to the end until the element is located or the boundaries are exhausted.
```python
def binary_search_brute(nums, target):
    for i in range(len(nums)):
        if nums[i] == target:
            return i
    return -1
```
* Optimized: Splitting the sorted search space in half dynamically during each iteration by comparing the target against the calculated midpoint index until bounds intersect.
```python
def binary_search(nums, target):
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
```
* Data structure used: No extra data structures allocated; handled exclusively with primitive index pointer tracking variables (`low`, `high`, `mid`).
* Complexity:
  * Brute Force: Time $O(n)$ due to potential full traversal; Space $O(1)$ since only a few pointer variables are used.
  * Optimized: Time $O(\log n)$ because the target search pool is reduced by exactly half at every execution step; Space $O(1)$ constant auxiliary footprint.
* Mistakes made: None. Successfully structured the edge constraints and index alterations independently on the first try.
* What I learned: When searching sorted domains, checking index configurations logarithmically delivers drastic performance wins over linear loops. Enforcing `low <= high` keeps the checking loop safe when handling arrays containing a single element or verifying boundary elements.

---

## Problem: Search Insert Position

* Brute force: Iterating through the sorted list sequentially to look for an element that is greater than or equal to the target value, returning its current position or the total length of the list.
```python
def search_insert_brute(nums, target):
    for i in range(len(nums)):
        if nums[i] >= target:
            return i
    return len(nums)
```
* Optimized: Applying binary search mechanics to narrow down the target location, where the lower pointer variable naturally stabilizes at the precise insert index location if the target does not exist.
```python
def search_insert(nums, target):
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
```
* Data structure used: Direct numerical pointer bounds trackers (`int`) for both brute force and optimization paths.
* Complexity:
  * Brute Force: Time $O(n)$ due to sequential traversal of the array; Space $O(1)$.
  * Optimized: Time $O(\log n)$ via logarithmic division; Space $O(1)$ constant workspace.
* Mistakes made: None. Successfully leveraged standard binary search boundaries to extract insertion behavior on the first attempt.
* What I learned: Binary search pointer convergence points provide incredibly useful secondary metadata. When a target cannot be found inside a `low <= high` verification loop, the `low` pointer automatically stops on the first index containing an element greater than the target—which is mathematically the exact insertion position needed to keep the array sorted.