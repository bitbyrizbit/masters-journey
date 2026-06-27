## Problem: Find First and Last Position of Element in Sorted Array

* Brute force: Scanning linearly from left to right to find the first occurrence of the target, then scanning from right to left to find the last occurrence, or running a single loop that caches all indices matching the target.
```python
def find_first_last_brute(nums, target):
    start, end = -1, -1
    for i in range(len(nums)):
        if nums[i] == target:
            if start == -1:
                start = i
            end = i
    return [start, end]
```
* Optimized: Running two distinct modified binary search passes; the first pass squeezes the upper bound inward to isolate the absolute leftmost index, and the second pass pushes the lower bound outward to freeze the absolute rightmost index.
```python
def find_first_last(nums, target):
    start, end = -1, -1
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] >= target:
            high = mid - 1
        else:
            low = mid + 1
    if low < len(nums) and nums[low] == target:
        start = low
    else:
        return [-1, -1] 
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] <= target:
            low = mid + 1
        else:
            high = mid - 1
    end = high
    return [start, end] 
```
* Data structure used: None; index range tracking variables (`low`, `high`, `mid`) are manipulated exclusively.
* Complexity:
  * Brute Force: Time $O(n)$ proportional to a standard sequential array sweep; Space $O(1)$.
  * Optimized: Time $O(\log n)$ because the target window is narrowed down logarithmically across two distinct binary searches; Space $O(1)$ constant auxiliary memory.
* Pattern Recognition:
  * Use bounded binary search passes when:
    - The array contains duplicate sorted elements, and you need to find the exact boundaries of a target block.
    - An exact match condition (`nums[mid] == target`) is insufficient because you need the maximum or minimum index of that group.
* Core Insight:
  Standard binary search exits early on any random match. By turning equal matches into boundary shifting signals—treating equality as a cue to drop `high` for the left search (`high = mid - 1`) and a cue to elevate `low` for the right search (`low = mid + 1`)—the pointers are mathematically forced to settle directly on the outer edges of the duplicated range.
* Mistakes made: The primary cognitive challenge was safely handling out-of-bounds pointer states when a target is entirely missing or greater than every item in the array. Constructing the protective boundary validation check `if low < len(nums) and nums[low] == target` right after the first loop was the key breakthrough to prevent index error crashes on missing target ranges.
* What I learned: Modifying binary search comparison thresholds shifts pointer post-conditions predictably. After the search loops terminate, the lower boundary pointer naturally locks onto the first element greater than or equal to the target, while the upper boundary pointer settles perfectly on the last element less than or equal to the target.

---

## Problem: Lower Bound and Upper Bound Frameworks

* Brute force: Sweeping the sorted list linearly to compare each element until finding the first value that is greater than or equal to the target (lower bound) or strictly greater than the target (upper bound).
```python
def lower_bound_brute(nums, target):
    for i in range(len(nums)):
        if nums[i] >= target: return i
    return len(nums)
```
* Optimized: Running specialized binary search functions that do not stop on an exact match, but instead use a state-saving variable (`result`) to remember valid midpoint indexes while using boundary cuts to hunt for even better edge alignments.
```python
def binary_search_exact(nums, target):
    low = 0
    high = len(nums) - 1    
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1            
    return -1

def lower_bound(nums, target):
    low = 0
    high = len(nums) - 1
    result = len(nums)
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] >= target:
            result = mid
            high = mid - 1
        else:
            low = mid + 1     
    return result

def upper_bound(nums, target):
    low = 0
    high = len(nums) - 1
    result = len(nums)
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] > target:
            result = mid
            high = mid - 1
        else:
            low = mid + 1  
    return result
```
* Data structure used: Primitive range boundary variables (`int`) used exclusively.
* Complexity:
  * Brute Force: Time $O(n)$ via sequential list scanning lines; Space $O(1)$.
  * Optimized: Time $O(\log n)$ because the search field drops logarithmically on each step; Space $O(1)$ constant workspace footprint.
* Pattern Recognition:
  * Use lower/upper bound architectures when:
    - You need to determine insertion slots, count element frequencies, or find structural range spans within a sorted array.
    - The task requires finding the "first element satisfying a condition" rather than an exact data variable.
* Core Insight:
  Standard binary search seeks a single node point, whereas lower and upper bounds search for array transition thresholds. By decoupling the loop from an early matching exit and caching promising indices into a persistent `result` tracker, the algorithm can aggressively clear the rest of the search pool without dropping the best answer found so far.
* Mistakes made: The thought-driven bottleneck was mastering the subtle conditional modification between the two bounds. The hardest challenge was recognizing that lower bound requires an inclusive target check (`nums[mid] >= target`) to catch the first duplicate, whereas upper bound requires a strict inequality check (`nums[mid] > target`) to skip past all duplicates and catch the first element beyond them.
* What I learned: Initializing the fallback state to `result = len(nums)` handles scenarios where the target is larger than everything in the list cleanly. These two code templates provide a universal, rock-solid framework for solving almost any search range problem efficiently.