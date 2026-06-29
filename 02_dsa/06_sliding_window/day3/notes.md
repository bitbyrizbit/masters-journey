## Problem: Longest Repeating Character Replacement

* Brute force: Checking every possible substring pair combinations using nested loops, counting the frequency of each character inside the substring, and calculating if the remaining characters can be replaced within the given budget `k`.
```python
def character_replacement_brute(s, k):
    max_length = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            substring = s[i:j]
            count = {}
            for char in substring:
                count[char] = count.get(char, 0) + 1
            max_freq = max(count.values()) if count else 0
            
            if (len(substring) - max_freq) <= k:
                max_length = max(max_length, len(substring))
    return max_length
```
* Optimized: Using a variable-size sliding window with a character frequency hash map, tracking the historical maximum frequency (`max_freq`) seen so far, and shrinking the window from the left only when the remaining character count exceeds `k`.
```python
def character_replacement(s, k):
    if not s:
        return 0
    count = {}
    max_length = 0
    max_freq = 0
    left = 0
    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_freq = max(max_freq, count[s[right]])
        if (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
        max_length = max(max_length, right - left + 1)        
    return max_length
```
* Data structure used: Standard Dictionary (`dict`) mapping `{char: int}` to track active window character frequencies for optimization.
* Complexity:
  * Brute Force: Time $O(n³)$ due to nested window sweeps multiplied by the inner dictionary frequency updates; Space $O(n)$ to store substring copies.
  * Optimized: Time $O(n)$ since the right pointer scans the string exactly once and the left pointer only moves forward incrementally; Space $O(m)$ where m is the number of unique characters in the alphabet (bounded by a constant of 26).
* Pattern Recognition:
  * Use an expandable sliding window with optimization tracking when:
    - You need to find the maximum contiguous sub-segment under an element-transformation allowance `k`.
    - Evaluating the global window state depends entirely on the dominant element inside that range.
* Core Insight:
  A valid window is one where the total number of characters we need to replace (`window_length - max_freq`) is less than or equal to `k`. Crucially, `max_freq` does not need to be decremented when the window shifts because a smaller frequency will never produce a substring longer than our current max length.
* Mistakes made: Initial difficulty was convincing myself that `max_freq` does not need to be recalculated or decreased when the left pointer moves forward and decrements a count. Realizing that `max_freq` only serves as a historical baseline anchor for the maximum possible window size was the hardest conceptual hurdle, as it completely eliminates the need to scan the dictionary values for a new max on every step.
* What I learned: Historical optimization constants can prevent expensive data re-scans. If a sliding window's validity depends on a maximum element, you only care when a new incoming element *beats* the previous peak, allowing you to bypass updating the state when the window contracts.

---

## Problem: Sliding Window Maximum

* Brute force: Sliding a pointer step-by-step across the array, slicing out a window of size `k` at each index, and running Python's built-in `max()` function to scan all elements within that slice from scratch.
```python
def sliding_window_max_brute(nums, k):
    if not nums or k > len(nums):
        return []
    output_list = []
    for i in range(len(nums) - k + 1):
        current_max = max(nums[i : i + k])
        output_list.append(current_max)
    return output_list
```
* Optimized: Utilizing a double-ended queue (deque) to maintain a monotonically decreasing sequence of element indices, ensuring the maximum value of the current active window is always positioned right at the front.
```python
from collections import deque

def sliding_window_max(nums, k):
    if not nums or k > len(nums):
        return []
        
    output_list = []
    q = deque()
    
    for i in range(len(nums)):
        if q and q[0] < i - k + 1:
            q.popleft()
            
        while q and nums[q[-1]] < nums[i]:
            q.pop()
            
        q.append(i)
        
        if i >= k - 1:
            output_list.append(nums[q[0]])
            
    return output_list
```
* Data structure used: List slicing for brute force; A Double-Ended Queue (`collections.deque`) tracking indices for optimization.
* Complexity:
  * Brute Force: Time $O(n \cdot k)$ due to running a linear maximum scan of size k across n windows; Space $O(1)$ auxiliary space if ignoring output allocations.
  * Optimized: Time $O(n)$ because each index is pushed into and popped from the deque at most once; Space $O(k)$ to buffer maximum indices inside the queue.
* Pattern Recognition:
  * Use a monotonic deque sliding window when:
    - You need to track the maximum or minimum element of a continuously moving window of size `k`.
    - Elements that enter the window can completely invalidate older, smaller elements behind them.
* Core Insight:
  If a new incoming element is larger than previous elements inside the window, those smaller elements can never be the maximum of the current or any future window. By aggressively popping smaller indices from the back of the deque before appending the new index, the largest active value naturally floats directly to the front.
* Mistakes made: Initial difficulty was implementing a list slicing approach combined with a raw lookup rule (`max(nums[start:end + 1])`). This forced the program to scan overlapping numbers repeatedly, introducing a hidden linear performance cost that scaled poorly on large arrays.
* What I learned: A monotonic deque converts a sliding maximum extraction routine into an O(1) constant time check. Storing index tracking pointers instead of raw values inside the queue allows you to easily identify and evict elements that have dropped out of the current spatial window.

---

## Problem: Minimum Size Subarray Sum

* Brute force: Evaluating every single potential starting and ending index combination using nested loops, calculating their subarray sums, and recording the shortest span that meets or exceeds the target.
```python
def min_size_subarray_brute(nums, target):
    min_length = float('inf')
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if sum(nums[i : j + 1]) >= target:
                min_length = min(min_length, j - i + 1)
    return min_length if min_length != float('inf') else 0
```
* Optimized: Running a dynamically resizing sliding window pass where the right pointer expands the total sum until it reaches the target threshold, which immediately triggers a nested `while` loop that contracts the left pointer to find the tightest valid boundary.
```python
def min_size_subarray(nums, target):
    if not nums:
        return 0 
    left = 0
    current_sum = 0
    min_length = float('inf')
    for right in range(len(nums)):
        current_sum += nums[right]
        while current_sum >= target:
            min_length = min(min_length, right - left + 1)
            current_sum -= nums[left]
            left += 1
    return min_length if min_length != float('inf') else 0
```
* Data structure used: None; primitive dynamic window boundary pointers (`left`, `right`) and tracking integers are managed directly.
* Complexity:
  * Brute Force: Time $O(n³)$ for this specific implementation because Python’s `sum(slice)` re-scans the subarray each time. A more careful brute force using incremental accumulation would reduce this to $O(n²)$; Space $O(1)$.
  * Optimized: Time $O(n)$ because both pointers move forward independently across the array index spectrum in a single pass; Space $O(1)$ constant auxiliary memory.
* Pattern Recognition:
  * Use a variable-sized dynamic sliding window when:
    - The problem asks for the minimum or maximum length of a contiguous subarray matching an inequality constraint.
    - The array elements are strictly positive, meaning window changes create a predictable, monotonic change in the sum.
* Core Insight:
  Instead of guessing window sizes, you expand the right pointer to find a valid subarray. The moment `current_sum >= target` is true, you freeze the expansion and use a `while` loop to shrink the left wall forward, actively shedding elements until the window breaks validity. This guarantees you discover the absolute smallest index span that hits the target sum.
* Mistakes made: The thought-driven bottleneck was designing a variable-size mechanism that doesn't rely on static step calculations. The challenge was ensuring that the inner left-pointer contraction loop (`while current_sum >= target`) can execute multiple times consecutively in a single right-pointer index jump to accurately squeeze out multiple unnecessary leading elements back-to-back when large values enter the right side.
* What I learned: Dynamic sliding windows utilize an expand-then-contract flow. By replacing nested loops with a rolling contraction logic (`current_sum -= nums[left]`), you ensure that every element is touched at most twice, providing a massive performance boost over static ranges.