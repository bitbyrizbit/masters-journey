## Problem: 3Sum

* Brute force: Using three nested loops to explore every possible triplet combination in the array, sorting each valid triplet to filter out duplicates, and adding unique sets to a results list.
```python
def three_sum_brute(nums):
    output_list = []
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    triplet = sorted([nums[i], nums[j], nums[k]])
                    if triplet not in output_list:
                        output_list.append(triplet)
    return output_list
```
* Optimized: Sorting the array first, fixing one number via a loop, and using two pointers moving inward to find the remaining pair (Two Sum II pattern), while skipping adjacent identical values to prevent duplicates.
```python
def three_sum(nums):
    nums.sort()
    output_list = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left = i + 1
        right = len(nums) - 1
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            if current_sum == 0:
                output_list.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif current_sum > 0:
                right -= 1  
            else:
                left += 1  
    return output_list
```
* Data structure used: Python List (`list`) for both approaches.
* Complexity:
  * Brute Force: In practice worse than O(N^3) due to duplicate membership checks; Space O(1) auxiliary memory (excluding output) or O(K) where K = number of valid triplets (including output)
  * Optimized: Time O(N^2) because a linear two-pointer scan runs inside a linear loop; Space O(1) or O(N) depending on the language's sorting memory footprint.
* Mistakes made: My early design attempt used an independent global two-pointer scan that calculated `0 - left - right` and checked for membership using `if complement in num_array`. This created multiple flaws: it accidentally counted the same element twice (self-duplication), skipped combinations prematurely by moving pointers based only on bounds, and forced an expensive `if sorted(...) not in output_list` check to clear duplicates.
* What I learned: You can safely transition a global three-variable problem into an isolated two-pointer search by anchoring the first item permanently inside a standard `for` loop. Skipping matching values actively via `nums[left] == nums[left + 1]` eliminates duplicate groups before they ever hit the output list, completely bypassing the need for heavy linear membership checks.

---

## Problem: Trapping Rain Water

* Brute force: Iterating through each index of the array and scanning the entire left and right subarrays from scratch to find the maximum wall heights on both sides, then calculating the trapped water for that cell.
```python
def trap_rain_water_brute(height):
    total_water = 0
    n = len(height)
    for i in range(1, n - 1):
        left_max = max(height[:i+1])
        right_max = max(height[i:])
        total_water += min(left_max, right_max) - height[i]
    return total_water
```
* Optimized: Maintaining two pointers at opposite ends of the array alongside two rolling scalar variables (`left_max` and `right_max`), moving the pointer with the shorter boundary inward to compute trapped water on the fly.
```python
def trap_rain_water(height):
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    total_water = 0
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            total_water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            total_water += right_max - height[right]
    return total_water
```
* Data structure used: Slicing buffers (`list`) for brute force; No extra data structures (Two-pointer indices and primitive numbers) for optimization.
* Complexity:
  * Brute Force: Time O(N^2); Space O(1) algorithmically (though Python slicing introduces temporary O(N) copies in this implementation).
  * Optimized: Time O(N) for a single linear pass traversing the terrain; Space O(1) constant auxiliary memory.
* Mistakes made: None. The main challenge was understanding the proof behind why the shorter boundary can be processed safely. 
* What I learned: The elevation profile of trapped water depends entirely on the bottlenecks of maximum boundary lines. By managing a two-pointer structural crunch, we can confidently determine trapped water sums from the shorter side because we know it is bounded by a confirmed larger wall on the opposing end, shifting space complexity from linear bounds down to a clean constant footprint.