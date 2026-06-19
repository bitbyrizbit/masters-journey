## Problem: Intersection of Two Arrays

* Brute force: Iterating through the first array and sequentially checking if each element exists in the second array, while filtering out duplicates.
```python
def intersection_brute(nums1, nums2):
    output_list = []
    for i in nums1:
        if i in nums2: 
            if i not in output_list:
                output_list.append(i)
    return output_list
```
* Optimized: Converting both arrays into set structures to instantly eliminate duplicates and finding their common elements using a built-in set intersection operator.
```python
def intersection_set(nums1, nums2):
    return list(set(nums1) & set(nums2))
```
* Data structure used: Python List (list) for brute force; Hash Set (set) for optimization.
* Complexity:
  * Brute Force: Time O(n × m) due to linear `in` scans on raw lists; Space O(min(n, m))
  * Optimized: Time O(n + m) on average for set conversions and lookups; Space O(n + m)
* Mistakes made: Brute-force works but scales poorly due to O(m) membership checks on lists.
* What I learned: Python sets use hash tables behind the scenes. This enables instant O(1) membership lookups and unlocks mathematical operations like the bitwise `&` operator to clean up code instantly.

---

## Problem: Longest Consecutive Sequence

* Brute force: Sorting the array first so that sequential items sit next to each other, then looping through to measure the length of consecutive runs.
```python
def lcs_brute(nums):
    if not nums:
        return 0
    nums.sort()
    longest_streak = 1
    current_streak = 1
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            continue
        elif nums[i] == nums[i-1] + 1:
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1
    return max(longest_streak, current_streak)
```
* Optimized: Storing all elements in a set and only initiating a count upward if the element is confirmed to be the absolute start of a sequence.
```python
def lcs_set(nums):
    num_set = set(nums)
    longest_streak = 0
    for num in num_set:
        if num - 1 not in num_set:
            current_num = num
            current_streak = 1
            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1  
            longest_streak = max(longest_streak, current_streak)
    return longest_streak
```
* Data structure used: Python List (list) with sorting for brute force; Hash Set (set) for optimization.
* Complexity:
  * Brute Force: Time O(n log n) due to the sorting step; Space O(1) or O(n) depending on python's internal sort allocation.
  * Optimized: Time O(n) because each unique number is visited at most twice; Space O(n)
* Mistakes made: Failing to account for duplicate numbers standing right next to each other in the sorted array, which broke the consecutive sequence tracking logic. Additionally, trying to track the sequences without using two separate streak counters (`current_streak` and `longest_streak`), which made it impossible to preserve the maximum length found when a sequence was interrupted.
* What I learned: A true O(n) runtime is achievable without sorting if you isolate the sequence bounds. Checking `if num - 1 not in num_set` ensures you only waste loop energy processing the actual beginnings of chains.

---

## Problem: Group Anagrams

* Brute force: Using nested loops to compare every word against every other word by checking their character frequencies manually, grouping matching words together, and tracking already grouped words to avoid duplicates.
```python
def group_anagrams_brute(anagrams):
    from collections import Counter
    visited = [False] * len(anagrams)
    result = []
    for i in range(len(anagrams)):
        if visited[i]:
            continue
        current_group = [anagrams[i]]
        visited[i] = True
        for j in range(i + 1, len(anagrams)):
            if not visited[j] and Counter(anagrams[i]) == Counter(anagrams[j]):
                current_group.append(anagrams[j])
                visited[j] = True
        result.append(current_group)
    return result
```
* Optimized: Iterating through the words once, sorting each word alphabetically to create a unique "signature" key, and grouping them inside a hash map using the signature.
```python
def group_anagrams_optimized(anagrams):
    groups = {}
    for word in anagrams:
        signature = "".join(sorted(word))
        if signature not in groups:
            groups[signature] = []
        groups[signature].append(word)
    return list(groups.values())
```
* Data structure used: A boolean tracking list (list) for brute force; Hash Map / Dictionary (`{str: [str]}`) for optimization.
* Complexity:
  * Brute Force: Time O(n² × k) due to nested loops comparing pairs of strings of length k; Space O(n) to store tracking flags.
  * Optimized: Time O(n × k log k) where sorting each string takes O(k log k) time; Space O(n × k) to hold hash table keys.
* Mistakes made: Implementing a logic that relied entirely on summing character weight values. This created a critical hashing collision defect; completely distinct words like "ad" (1 + 4 = 5) and "bc" (2 + 3 = 5) yielded identical scores, causing the program to incorrectly group non-anagram elements together.
* What I learned: Character score calculations suffer from hash collisions and cannot prove string equivalence on their own. Sorting string characters alphabetically acts as a foolproof signature method because true anagrams always boil down to the exact same sequence when sorted.
