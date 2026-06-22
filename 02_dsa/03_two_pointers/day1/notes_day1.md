## Problem: Valid Palindrome

* Brute attempt: Reversing the raw input string without filtering non-alphanumeric characters first, then comparing case-insensitively. This works only for plain strings and fails on inputs containing punctuation or spaces.
```python
def valid_palindrome_brute(s):
    reversed_s = ""
    # Manually reverse the raw input string character by character
    for char in range(len(s) - 1, -1, -1):
        reversed_s += s[char]
    return s.lower() == reversed_s.lower()
```
* Optimized: Using a two-pointer approach to scan inwards from both ends simultaneously, skipping non-alphanumeric characters on the fly and comparing values directly in a single pass.
```python
def valid_palindrome_two_pointer(s):
    left = 0
    right = len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```
* Data structure used: String buffer accumulation for brute force; No extra data structure (Two-pointer variables) for optimization.
* Complexity:
  * Brute Force: Time O(n^2) in this implementation due to repeated string concatenation inside the loop; Space O(n).
  * Optimized: Time O(n) as each character is scanned at most twice; Space O(1) auxiliary constant memory.
* Mistakes made: Initially relying on a messy chain of `.lower()` and `.replace()` operations to sanitize the string format for the brute force logic instead of cleanly utilizing the built-in `.isalnum()` string validator function.
* What I learned: Built-in string methods like `.isalnum()` drastically simplify input filtering. Furthermore, moving pointers inward based on validation rules bypasses the need to create new string buffers in memory, shifting space efficiency from linear to constant.

---

## Problem: Two Sum II - Input Array Is Sorted

* Brute force: Running nested loops to evaluate the sum of every possible combination of element pairs in the array until the target matches.
```python
def two_sum_sorted_brute(numbers, target):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]
```
* Optimized: Leveraging the sorted property of the array with two pointers at the boundaries, adjusting the search space inward based on whether the current sum is greater or less than the target value.
```python
def two_sum_sorted(numbers, target):
    left = 0
    right = len(numbers) - 1
    while left < right:
        if numbers[left] + numbers[right] > target: 
            right -= 1 
        elif numbers[left] + numbers[right] < target: 
            left += 1
        else: 
            return [left + 1, right + 1]
```
* Data structure used: No extra data structures allocated; managed exclusively with two index pointer trackers.
* Complexity:
  * Brute Force: Time O(n^2) due to the nested loops checking all index pairings; Space O(1) constant memory.
  * Optimized: Time O(n) for a single linear pass over the sorted elements; Space O(1) constant memory.
* Mistakes made: None.
* What I learned: When an array is already sorted, you can eliminate large portions of the search space instantly. Comparing bounds gives complete control over value directional shifts: lowering the upper pointer reduces the total sum, while elevating the lower pointer increases it.

---

## Problem: Container With Most Water

* Brute force: Using nested loops to evaluate the capacity bounds of every single pair of vertical lines in the height array to figure out the ultimate maximum area.
```python
def container_brute(heights):
    max_area = 0
    for i in range(len(heights)):
        for j in range(i + 1, len(heights)):
            width = j - i
            height = min(heights[i], heights[j])
            area = width * height
            max_area = max(max_area, area)
    return max_area
```
* Optimized: Using two pointers at both ends of the array, computing area at each step, and moving the pointer at the shorter line inward because only that move can potentially increase height enough to offset shrinking width.
```python
def container(heights):
    left = 0 
    right = len(heights) - 1
    max_area = 0
    while left < right:
        width = right - left
        height = min(heights[right], heights[left])
        area = width * height
        if area > max_area:
            max_area = area 
        if heights[left] < heights[right]:
            left += 1 
        else: 
            right -= 1
    return max_area
```
* Data structure used: No extra data structures used for the correct brute force loop setup; Two integer pointers (`left`, `right`) and a scalar tracker (`max_area`)
* Complexity:
  * Brute Force: Time O(n^2) due to nested iteration configurations scanning pairs; Space O(1).
  * Optimized: Time O(n) as pointers move incrementally closer; Space O(1) constant space execution.
* Mistakes made: Allocating an external output_list to append every single calculated water area value sequentially, forcing a linear memory footprint (O(n) space complexity) when the tracking step can be resolved via an instant constant-space scalar check.
* What I learned: You do not need to preserve historical data structures if your final objective is a singular extreme limit like a maximum or minimum. Evaluating values sequentially against an independent scalar variable preserves identical logical thresholds while shedding linear memory baggage. In two-pointer optimization, moving the taller line is never beneficial when the shorter line is the bottleneck, because width decreases while limiting height stays unchanged or worse.