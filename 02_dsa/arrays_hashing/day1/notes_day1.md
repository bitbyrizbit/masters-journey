## Problem: Contains Duplicate

* Brute force: Iterated through the array and tracked visited numbers using an external Python list, checking membership sequentially.
```python
unique = []
def contains_duplicate_brute(arr):
    for i in arr:
        if i in unique: return True
        unique.append(i)
    return False
```
* Optimized: Used a set structure to eliminate duplicates instantly, then compared the length of the set against the length of the original list. Set gives fast O(1) average lookup, making duplicate detection efficient. 
```python
def contains_duplicate_set(arr):
    unique = set(arr)
    return len(unique) != len(arr)
```
* Data structure used: Python List (list) for brute force; Hash Set (set) for optimization. 
* Complexity:
  * Brute Force: Time O(n²) due to sequential in lookups on a list; Space O(n)
  * Optimized: Time O(n) to construct the set; Space O(n)
* Mistakes made: Declaring the unique list outside the function scope. This created a persistent global state, causing subsequent independent function calls to retain old data and return false positives.
* What I learned: Keeping state tracking structures inside function scopes prevents cross-contamination between test runs. Using set() length comparisons is a clean, pythonic way to identify duplicates in a single operation.

---

## Problem: Valid Anagram

* Brute force: Manually counting character frequencies using a standard loop and a normal dictionary, or sorting both strings directly.
```python 
def anagram_brute(s, t):
    if len(s) != len(t): return False
    count = {}
    for char in s:
        count[char] = count.get(char, 0) + 1
    for char in t:
        if char not in count or count[char] == 0: return False
        count[char] -= 1
    return True
```
* Optimized: Use Counter to build frequency maps of both strings and compare them directly.
```python 
from collections import Counter
def anagram(s, t):
    return Counter(s) == Counter(t)
```
* Data structure used: Standard Dictionary (dict) for brute force; Hash Map Bag container (collections.Counter) for optimization.
* Complexity:
  * Brute Force (Manual Dict): Time O(n), Space O(k)
  **Note:** While the time complexity is theoretically O(n), doing it manually in pure Python loops is slower than Counter.
  * Optimized (Counter): Time O(n), Space O(k) (where k is the number of unique characters).
* Mistakes made: Relying purely on Counter(s) - Counter(t) without a string length check. Because Counter subtraction silently deletes keys with values of zero or less, a longer string containing extra characters ("listennn") would falsely register as an anagram of a shorter string ("listen").
* What I learned: Counter math operators drop non-positive values automatically. Adding a simple len(s) != len(t) guard clause handles these edge cases reliably when using subtraction mechanics.

---

## Problem: Two Sums

* Brute force: Using nested loops to check the sum of every possible pair of elements in the array.
```python
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return [] 
```
* Optimized: Tracked numbers and indices simultaneously in a single pass using a hash map lookup for complements.
```python
def two_sum(nums, target):
    seen = {}
    for index, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], index]
        seen[num] = index
```
* Data structure used: No extra data structure for brute force; Hash Map / Dictionary (dict) for optimization.
* Complexity:
  * Brute Force: Time O(n^2) due to the nested loop scanning; Space O(1) as no extra memory is allocated.
  * Optimized: Time O(n) for a single-pass loop traversal; Space O(n) to store seen entries.
* Mistakes made: Original attempt used an un-indexed while loop that didn't progress its parameters, trapping execution in an infinite loop. Thus, final implementation completely resolved this by tracking past items cleanly.
* What I learned: The single-pass lookup technique dynamically turns a value lookup into a history lookup. Instead of scanning ahead for what you need, you look backward at what you have already collected.