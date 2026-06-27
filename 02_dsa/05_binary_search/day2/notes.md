## Problem: Search in Rotated Sorted Array

* Brute force: Performing a standard linear scan across the entire array from index 0 to the end to locate the target value, completely ignoring the rotation pivot or sorted properties.
```python
def search_rotated_brute(nums, target):
    for i in range(len(nums)):
        if nums[i] == target:
            return i
    return -1
```
* Optimized: Running a modified binary search where on each iteration, we identify which half of the array is normally sorted (left or right) and check if the target falls within that sorted range to shift boundaries.
```python
def search(nums, target):
    if not nums:
        return -1
    low = 0 
    high = len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        if nums[low] <= nums[mid]:
            if nums[low] <= target < nums[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            if nums[mid] < target <= nums[high]:
                low = mid + 1
            else:
                high = mid - 1
    return -1 
```
* Data structure used: None; managed using primitive index trackers (`low`, `high`, `mid`).
* Complexity:
  * Brute Force: Time $O(n)$ due to full element scanning paths; Space $O(1)$ constant memory.
  * Optimized: Time $O(\log n)$ because each iteration guarantees at least one half is sorted, allowing elimination of roughly half the search space (logarithmic truncation); Space $O(1)$ constant workspace.
* Pattern Recognition:
  * Use binary search on rotated domains when:
    - The sequence is partitioned into two sorted segments separated by a single inflection point.
    - You can systematically rule out half of the search pool by comparing the midpoint against boundary elements.
* Binary Search Type: Modified binary search on rotated array
* Core Insight:
  In a rotated sorted array with distinct values, at least one half around mid is guaranteed to remain sorted. By validating the sorted half first, you can conclusively determine if the target lies within its boundaries or must exist in the remaining shifted section.
* Mistakes made: The primary cognitive hurdle was figuring out how to structure the conditional boundary logic without dropping elements when an array shrinks down to just two numbers (like `nums = [3, 1]`, `target = 1`). Realizing that the check must be inclusive of the boundary (`nums[low] <= nums[mid]`) was the hardest conceptual hurdle, as missing the equality sign breaks index routing on small list frames.
* What I learned: Binary search logic handles rotated lists cleanly if you evaluate sorted subsets first. Enforcing strict inclusive comparisons (`<=`) prevents the pointers from skipping valid elements during convergence.

---

## Problem: Find Minimum in Rotated Sorted Array

* Brute force: Traversing the entire list sequentially to locate the single absolute smallest element or scanning for the specific point where an element is suddenly smaller than its predecessor.
```python
def findMin_brute(nums):
    return min(nums)  # Full linear O(n) scan
```
* Optimized: Utilizing a binary search layout that constantly compares the midpoint value against the rightmost boundary value, forcing the bounds to shrink and wrap around the inflection point.
```python
def findMin(nums):
    if not nums:
        return -1
    low = 0
    high = len(nums) - 1
    while low < high:
        mid = (low + high) // 2
        if nums[mid] > nums[high]:
            low = mid + 1
        else:
            high = mid
    return nums[low]
```
* Data structure used: Linear index bounds trackers (`int`) for optimization paths.
* Complexity:
  * Brute Force: Time $O(n)$ via linear minimum scanning loops; Space $O(1)$.
  * Optimized: Time $O(\log n)$ through logarithmic range narrowing; Space $O(1)$ constant memory footprint.
* Pattern Recognition:
  * Use binary search convergence when:
    - You are searching for the structural pivot or absolute minimum inflection point in a modified sorted loop.
    - The right boundary element serves as a stable anchor point for comparison rather than a fixed target value.
* Binary Search Type: Boundary convergence / pivot search
* Core Insight:
  If the middle element is greater than the rightmost element (`nums[mid] > nums[high]`), it mathematically proves that the inflection pivot (and the absolute minimum value) must reside strictly in the right section, allowing you to discard the entire left half.
* Mistakes made: My initial instinct was to compare nums[mid] against nums[low], but this made pointer movement harder to reason about in squeezed windows. Switching to nums[high] gave a much cleaner directional signal. Shifting the anchor reference to always check against the right boundary (`nums[high]`) resolved this blind spot perfectly.
* What I learned: Comparing middle values against the right boundary elements provides a foolproof directional signal in rotated arrays. Setting `high = mid` rather than `mid - 1` ensures that the midpoint itself isn't discarded when it is a potential candidate for the minimum value.

---

## Problem: Koko Eating Bananas

* Brute force: Testing every possible integer eating speed starting from 1 banana per hour upwards, calculating the total hours required for each candidate rate until finding the first speed that fits within the target hour limit `h`.
```python
import math

def minEatingSpeed_brute(piles, h):
    speed = 1
    while True:
        total_hours = sum(math.ceil(pile / speed) for pile in piles)
        if total_hours <= h:
            return speed
        speed += 1
```
* Optimized: Applying a "Binary Search on Answer" technique across the feasible numeric speed range from 1 up to the maximum pile value, minimizing the valid eating speed logarithmically.
```python
import math

def minEatingSpeed(piles, h):
    low = 1
    high = max(piles)
    while low < high:
        mid = (low + high) // 2
        total_hours = 0
        for pile in piles:
            total_hours += math.ceil(pile / mid)
        if total_hours <= h:
            high = mid
        else:
            low = mid + 1
    return low
```
* Data structure used: None; mathematical numeric range scalar trackers (`int`) are used exclusively.
* Complexity:
  * Brute Force: Time $O(m \cdot n)$ where $m$ is the maximum value in piles and $n$ is the length of piles; Space $O(1)$.
  * Optimized: Time $O(n \log m)$ where $n$ is the number of piles and $m$ is the maximum pile height value, as we run an $O(n)$ loop inside an $O(\log m)$ range tracker; Space $O(1)$ constant auxiliary memory.
* Pattern Recognition:
  * Use Binary Search on Answer when:
    - The problem asks for a minimum or maximum possible threshold value to satisfy a condition.
    - The target answer range is strictly bounded (between 1 and `max(piles)`).
    - The total cost function is monotonic (increasing the eating speed always reduces or maintains total hours).
* Binary Search Type: Binary Search on Answer
* Core Insight:
  Instead of treating piles as a list to be searched, the true search domain is the continuous sequence of potential eating speeds. Since calculating the total hours spent creates a clean monotonic curve, we can use binary search to narrow down the exact threshold speed where the hour constraint is satisfied.
* Mistakes made: The primary cognitive hurdle was realizing that Koko cannot carry over leftover eating capacities between hours (e.g., eating a pile of 3 at speed 4 still consumes a full 1 hour block). This required changing normal division loops into ceiling division calculations using `math.ceil(pile / mid)` to simulate realistic hourly restrictions correctly.
* What I learned: Using ceiling division is essential for modeling independent time slots. Using a convergence style loop condition (`low < high`) combined with anchoring `high = mid` allows the search space to shrink gracefully, ensuring the lower pointer settles directly on the absolute minimum speed threshold that works.