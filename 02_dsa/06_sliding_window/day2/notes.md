## Problem: Maximum Sum Subarray of Size K

* Brute force: Using nested loops to inspect every possible starting position in the array, slicing out a contiguous sub-segment of length $K$, and summing up its elements from scratch to locate the maximum total.
```python
def subarray_brute(nums, k):
    max_sum = 0
    for i in range(len(nums) - k + 1):
        current_sum = sum(nums[i : i + k])
        max_sum = max(max_sum, current_sum)
    return max_sum
```
* Optimized: Maintaining a rolling sum variable over a fixed window size of $K$, shifting the boundaries linearly by adding the new incoming element on the right and subtracting the outgoing element on the left in constant time.
```python
def subarray(nums, k):
    if not nums or k > len(nums):
        return 0
    
    # Pre-calculate the sum of the very first window
    current_sum = sum(nums[:k])
    max_sum = current_sum
    
    # Slide the window across the remaining elements
    for i in range(k, len(nums)):
        current_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, current_sum)
        
    return max_sum
```
* Data structure used: List slicing for brute force; A single rolling accumulation variable (`int`) for optimization.
* Complexity:
  * Brute Force: Time $O(n \cdot k)$ due to re-summing subarray blocks inside a traversal loop; Space $O(1)$ constant workspace footprint.
  * Optimized: Time $O(n)$ since each individual element is processed at most twice in a single linear pass; Space $O(1)$ constant auxiliary memory.
* Pattern Recognition:
  * Use a fixed-size sliding window when:
    - The problem requires tracking contiguous sub-segments of a constant, predefined length $K$.
    - Re-computing the historical aggregate values (sums, products, averages) of overlapping scopes creates a processing bottleneck.
* Core Insight:
  When a fixed window of size $K$ shifts one step forward, $K-1$ elements remain completely unchanged. Instead of wasting energy summing those elements from scratch, you can update the total instantly by executing a rolling exchange: add the fresh incoming element on the right and subtract the dropped element on the left.
* Mistakes made: Initial difficulty was relying on a dynamic list slice summation structure (`sum(nums[start:end + 1])`) inside the loop. This forced Python to re-copy and re-add overlapping indices on every single iteration, introducing a hidden linear calculation multiplier that compromised the overall time complexity.
* What I learned: Slicing buffers inside looping routines creates hidden execution drains. Tracking a rolling mathematical delta variable preserves linear efficiency, dropping code overhead from a quadratic multiplier down to a clean constant-time operation.

---

## Problem: Permutation in String

* Brute force: Generating all possible permutations of string `s1` manually, and running a sequential string match lookup to check if any of those combinations exist inside `s2`.
```python
import itertools

def permutation_brute(s1, s2):
    # Generating all permutations of s1 takes factorial O(K!) time, which crashes on medium strings.
    all_perms = ["".join(p) for p in itertools.permutations(s1)]
    for perm in all_perms:
        if perm in s2:
            return True
    return False
```
* Optimized: Running a fixed-size sliding window across `s2` that mirrors the length of `s1`, utilizing a frequency map to track the active character window and deleting keys on the fly when their counts drop to zero to allow direct map comparisons.
```python
from collections import Counter

def permutation(s1, s2):
    k = len(s1)
    target = Counter(s1)
    window = Counter(s2[:k])
    
    for i in range(k, len(s2)):
        if target == window:
            return True
        window[s2[i]] += 1
        left_char = s2[i - k]
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]            
    return target == window
```
* Data structure used: None for brute force; Frequency hash maps (`collections.Counter`) for optimization.
* Complexity:
  * Brute Force: Time $O(k! + n)$ where $k$ is the length of `s1` and $n$ is the length of `s2`; Space $O(k!)$ to hold permutation sequences.
  * Optimized: Time $O(n)$ since dictionary modifications run in constant time over a single sweep of `s2`; Space $O(m)$ where $m$ is the unique character set alphabet size (max $O(1)$ bounded by 26 characters).
* Pattern Recognition:
  * Use an anagram-matching sliding window when:
    - You need to determine if a string contains any scrambled arrangement or permutation of a target string.
    - The problem constraints require sequence tracking where specific character frequency balances must match exactly.
* Core Insight:
  An anagram or permutation depends entirely on identical character counts, regardless of their actual placement order. By managing a frequency tracker over a sliding window, you can verify if a segment matches by running a direct map comparison (`target == window`). Explicitly purging keys using `del` when they hit a count of zero is mandatory to prevent obsolete markers from corrupting map equality checks.
* Mistakes made: None. Independently designed the constant-time sliding map optimization step and correctly incorporated the key cleanup validation `del window[left_char]` to guarantee accurate object equality evaluations on every iteration.
* What I learned: Python dictionary comparisons check both keys and values for exact parity. If a character count drops to zero but the key remains in the dictionary, the map equality check will fail against a target dictionary that lacks that key. Actively cleaning up empty slots keeps frequency vectors perfectly synchronized.

---

## Problem: Minimum Window Substring

* Brute force: Generating every possible varying substring combination from `s` using nested loops, and verifying if each candidate substring contains all required character frequencies specified in `t`.
```python
from collections import Counter

def min_window_brute(s, t):
    target = Counter(t)
    min_len = float('inf')
    ans = ""
    for i in range(len(s)):
        for j in range(i + len(t), len(s) + 1):
            window = Counter(s[i:j])
            # Check if window satisfies all requirements of target
            if all(window[char] >= target[char] for char in target):
                if (j - i) < min_len:
                    min_len = j - i
                    ans = s[i:j]
    return ans
```
* Optimized: Driving an expandable sliding window via an active integer array map where the right pointer expands to collect elements, and a dynamic variable `missing` tracks completeness to trigger a tight inner left-pointer contraction loop.
```python
def min_window(s, t):
    target = [0] * 128
    for char in t:
        target[ord(char)] += 1
    missing = len(t)
    start = 0
    ans_start = 0
    min_len = float('inf')
    
    for end in range(len(s)):
        right_char = ord(s[end])
        if target[right_char] > 0:
            missing -= 1
        target[right_char] -= 1
        
        while missing == 0:
            if (end - start + 1) < min_len:
                min_len = end - start + 1
                ans_start = start
            left_char = ord(s[start])
            target[left_char] += 1
            if target[left_char] > 0:
                missing += 1
            start += 1
            
    return s[ans_start : ans_start + min_len] if min_len != float('inf') else ""
```
* Data structure used: Full hash map constructions for brute force; A fixed-size primitive integer lookup array (`list` of size 128) acting as a direct-address table for optimization.
* Complexity:
  * Brute Force: Time $O(n^3)$ due to nested window generation paired with sub-character map scans; Space $O(n + m)$.
  * Optimized: Time $O(n + m)$ where $n$ is the size of string `s` and $m$ is the size of string `t`, as both pointers move from left to right in a single linear pass; Space $O(1)$ auxiliary constant space bounded strictly by the fixed 128 ASCII character array slots.
* Pattern Recognition:
  * Use a variable-size sliding window with match throttling when:
    - You need to find the absolute smallest or largest continuous sub-segment that satisfies a collection of multi-element criteria.
    - The structural constraint requires tracking dynamic, multi-tier count boundaries that flex inward and outward on the fly.
* Core Insight:
  Instead of comparing whole dictionary objects repeatedly, you can manage a single scalar tracker `missing` that records exactly how many character requirements remain unfulfilled. Expand the right side to capture characters and decrement counts. The moment `missing` reaches 0, you freeze the right side and aggressively squeeze the left pointer forward to shed unneeded characters, uncovering the tightest possible valid window sub-segment.
* Mistakes made: None. Implemented the fixed 128 ASCII direct-address index mapping layout and managed the dual-pointer lookup expansion/contraction flow.
* What I learned: Substituting heavy high-level object classes like `Counter` with a raw integer array (`[0] * 128`) using `ord(char)` bypasses hashing overhead entirely, accelerating code execution speeds drastically. Utilizing a dedicated matching flag (`missing`) enables instant constant-time validation checks, converting a complex structural alignment problem into a clean, blazing-fast linear pass.