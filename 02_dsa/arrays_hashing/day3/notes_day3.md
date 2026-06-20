## Problem: Running Sum of 1D Array

* Brute force: Slicing the array up to the current index during each iteration and using the `sum()` function to calculate the total from scratch every time.
```python
def running_sum(nums):
    output_list = []
    for i in range(1, len(nums) + 1):
        total = sum(nums[:i])
        output_list.append(total)
    return output_list
```
* Optimized: Iterating through the array once and keeping a rolling total variable that adds the current number to the previous sum, eliminating redundant addition operations.
```python
def running_sum_optimized(nums):
    output_list = []
    current_sum = 0
    for num in nums:
        current_sum += num
        output_list.append(current_sum)
    return output_list
```
* Data structure used: Python List (list) for both approaches.
* Complexity:
  * Brute Force: Time O(n^2) because slicing takes O(k) and summing elements inside a loop creates quadratic overhead; Space O(n).
  * Optimized: Time O(n) for a single-pass traversal; Space O(n) because output list stores n elements or O(1) auxiliary if output excluded. 
* Mistakes made: Slicing the list with `nums[:i]` inside the loop, which forces Python to re-copy and re-add the same elements repeatedly instead of reusing the previously calculated total. Basically, each iteration recomputes work already done in previous iterations.
* What I learned: Tracking a rolling cumulative sum variable converts a slow slice-and-sum loop into a fast single-pass operation, reducing the time complexity from quadratic to linear.

---

## Problem: Subarray Sum Equals K

* Brute force: Checking every possible contiguous subarray using nested loops to calculate their sums and checking if they equal the target value `k`.
```python
def subarray_sum_brute(nums, k):
    count = 0
    for i in range(len(nums)):
        current_sum = 0
        for j in range(i, len(nums)):
            current_sum += nums[j]
            if current_sum == k:
                count += 1
    return count
```
* Optimized: Using a single pass to build a rolling prefix sum and checking a hash map to see if the complement value (`current_sum - k`) was encountered previously.
```python
def subarray_sum(nums, k):
    count = 0 
    current_sum = 0
    prefix_sum = {0: 1}
    for num in nums:
        current_sum += num
        if current_sum - k in prefix_sum:
            count += prefix_sum[current_sum-k]
        prefix_sum[current_sum] = prefix_sum.get(current_sum, 0) + 1
    return count
```
* Data structure used: No extra data structure for brute force; Hash Map / Dictionary (dict) for optimization to track prefix sum frequencies.
* Complexity:
  * Brute Force: Time O(n^2) due to nested loops exploring all subarray combinations; Space O(1).
  * Optimized: Time O(n) as dictionary lookups run in constant time; Space O(n) to store prefix sum frequencies.
* Mistakes made: Forgetting that a prefix sum can occur multiple times when an array contains zeros or negative integers, meaning you must add the frequency count `prefix_sum[current_sum-k]` rather than increments of 1.
* What I learned: The prefix sum technique maps array totals to a hash table. By checking if a past prefix sum matches `current_sum - k`, you can identify valid contiguous segments instantly without scanning backward.

---

## Problem: Product of Array Except Self

* Brute Attempt: My initial brute attempt recalculated total product for every index, making it O(n^2) 
```python
import math
def product_except_self_brute(nums):
    output_list = []
    for i in range(len(nums)):
        product = math.prod(nums)
        current_prod = product // nums[i]
        output_list.append(current_prod)
    return output_list
```
* Optimized: Running two separate sequential loops to compute the cumulative products coming from the left side (prefixes) and the right side (suffixes) directly into a single output array.
```python
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
```
* Data structure used: Python List (list) for both approaches.
* Complexity:
  * Brute Attempt: Time O(n^2) because evaluating `math.prod(nums)` inside a loop scans the list fully on each iteration; Space O(1).
  * Optimized: Time O(n) because it uses two independent linear passes; Space O(1) auxiliary space if the output array does not count toward complexity.
* Mistakes made: Using division logic (`// nums[i]`), which triggers a runtime crash due to a `ZeroDivisionError` if the array contains a zero. Additionally, recalculating the full product inside the loop elevated the execution time to O(n^2).
* What I learned: Division shorthand breaks down when handling elements containing zero. Splitting the problem into an independent prefix pass and an inverted suffix pass calculates products safely and preserves O(n) efficiency.
