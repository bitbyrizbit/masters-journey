## Problem: Longest Substring with At Most K Distinct Characters

* Brute force: Generating every possible substring combination using nested loops, converting each substring into a set to evaluate the count of unique characters, and keeping track of the maximum valid window length.
```python
def distinct_substring_brute(s, k):
    max_length = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            substring = s[i:j]
            if len(set(substring)) <= k:
                max_length = max(max_length, len(substring))
    return max_length
```
* Optimized: Using a variable-size sliding window with a character frequency hash map, expanding the right pointer to ingest characters, and triggering a continuous left pointer contraction loop whenever the size of the map exceeds `k`.
```python
def distinct_substring(s, k):
    if not s or k == 0:
        return 0
    char_map = {}
    left = 0
    max_length = 0
    for right in range(len(s)):
        char_map[s[right]] = char_map.get(s[right], 0) + 1
        while len(char_map) > k:
            char_map[s[left]] -= 1
            if char_map[s[left]] == 0:
                del char_map[s[left]]
            left += 1
        max_length = max(max_length, right - left + 1)
    return max_length
```
* Data structure used: None for brute force; Standard Dictionary (`dict`) mapping `{char: int}` to track distinct character frequencies within the active window for optimization.
* Complexity:
  * Brute Force: Time $O(n^3)$ due to nested window extraction combined with inner set allocations; Space $O(n)$ to house copy slices.
  * Optimized: Time $O(n)$ since the right pointer drives a single pass and the left pointer crawls forward incrementally without backtracking; Space $O(k)$ to store up to $k + 1$ unique character records inside the tracking map.
* Pattern Recognition:
  * Use a dynamic sliding window with unique element filters when:
    - The structural constraint limits the diversity or count of unique element types (`len(char_map) > k`).
    - The target optimization requires maximizing a contiguous slice under a hard category threshold.
* Core Insight:
  A hash map's length (`len(char_map)`) represents the exact number of distinct characters in the current window. When an incoming character introduces a $(k+1)$-th distinct type, the window becomes invalid. To restore validity, slide the left pointer forward, decrementing character counts, and actively purge keys from the map with `del` the moment their frequency drops to zero.
* Mistakes made: The primary cognitive challenge was managing map integrity during window contraction. The design bottleneck was ensuring that dropping a frequency count to zero explicitly triggers key deletion (`del char_map[s[left]]`), because leaving a key with a value of `0` inside the map would cause `len(char_map)` to return an inflated count, permanently breaking the loop's validity checks.
* What I learned: Dictionary equality and size lookups depend strictly on key membership, not values. Actively cleaning up empty collection slots keeps size dimensions synchronized with the physical sliding window spectrum in constant time.

---

## Problem: Fruit Into Baskets

* Brute force: Evaluating every possible consecutive subarray combinations of trees using nested loops, checking if the segment contains at most 2 distinct types of fruit, and tracking the maximum count of collected fruit.
```python
def fruits_in_basket_brute(fruits):
    max_length = 0
    for i in range(len(fruits)):
        for j in range(i + 1, len(fruits) + 1):
            if len(set(fruits[i:j])) <= 2:
                max_length = max(max_length, j - i)
    return max_length
```
* Optimized: Running an identical expandable sliding window structure that maps unique fruit types to an internal frequency dictionary, throttling expansions via left-pointer contractions the moment the map length exceeds a static threshold of 2 baskets.
```python
def fruits_in_basket(fruits):
    if not fruits:
        return 0
    char_map = {}
    left = 0
    max_length = 0
    for right in range(len(fruits)):
        char_map[fruits[right]] = char_map.get(fruits[right], 0) + 1
        while len(char_map) > 2:
            char_map[fruits[left]] -= 1
            if char_map[fruits[left]] == 0:
                del char_map[fruits[left]]
            left += 1
        max_length = max(max_length, right - left + 1)
    return max_length
```
* Data structure used: A frequency Hash Map (`dict`) tracking `{fruit_type: frequency}` bounds for optimization.
* Complexity:
  * Brute Force: Time $O(n^3)$ due to full subarray extractions and set evaluations; Space $O(n)$.
  * Optimized: Time $O(n)$ for a single linear pass traversing the tree sequence; Space $O(1)$ constant auxiliary space since the map is constrained to hold at most 3 distinct keys at any given time.
* Pattern Recognition:
  * Use a dynamic sliding window with a fixed threshold when:
    - A word-problem scenario maps directly to structural array limitations (e.g., "2 baskets" mathematically translates to "at most 2 unique elements").
    - The input array represents a contiguous processing stream where you must maximize sequential collections.
* Core Insight:
  Despite the unique story dressing, "Fruit Into Baskets" is completely isomorphic to the "Longest Substring with At Most K Distinct Characters" problem where $k = 2$. Recognizing this underlying code structure allows you to reuse the exact same dynamic sliding window template without changes.
* Mistakes made: The thought-driven bottleneck was abstracting the narrative description into a pure data structure problem. Translating physical objects (baskets, trees, fruits) into map state boundaries (`len(char_map) > 2`) required stripping away the problem's thematic dressing to uncover the exact sliding pattern beneath it.
* What I learned: Many algorithmic questions are simply semantic variations of core foundational patterns. Recognizing structural problem identity allows you to deploy proven code structures instantly, bypassing the need to invent a custom tracking routine from scratch.

---

## Problem: Subarrays with K Distinct Integers

* Brute force: Checking every single potential contiguous subarray combination using nested loops, converting each slice into a set, and incrementing a global counter whenever a slice contains exactly `k` distinct integers.
```python
def subarray_k_distinct_brute(nums, k):
    count = 0
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n + 1):
            if len(set(nums[i:j])) == k:
                count += 1
    return count
```
* Optimized: Leveraging a mathematical reduction function `atMost(goal)` that calculates the number of subarrays with *at most* a specific number of distinct integers, returning the exact boundary match by computing `atMost(k) - atMost(k - 1)`.
```python
def subarray_k_distinct(nums, k):
    def atMost(goal):
        if goal == 0:
            return 0
        counts = {}
        left = 0
        ans = 0
        for right in range(len(nums)):
            counts[nums[right]] = counts.get(nums[right], 0) + 1
            while len(counts) > goal:
                counts[nums[left]] -= 1
                if counts[nums[left]] == 0:
                    del counts[nums[left]]
                left += 1
            ans += right - left + 1
        return ans
    return atMost(k) - atMost(k - 1)
```
* Data structure used: Nested loops for brute force; Iterative sliding window frequency dictionaries (`dict`) inside a mathematical helper function for optimization.
* Complexity:
  * Brute Force: Time $O(n^3)$ due to inspecting all sliding combinations paired with inner set calculations; Space $O(n)$.
  * Optimized: Time $O(n)$ because the linear `atMost` helper executes exactly twice back-to-back; Space $O(k)$ average, $O(n)$ worst case depending on distinct integers inside active window.
* Pattern Recognition:
  * Use the exact-match reduction pattern (`atMost(k) - atMost(k - 1)`) when:
    - The sliding window problem requires finding subarrays matching an *exact* count condition (`exactly K`), rather than an inequality bound (`at most` or `at least`).
    - Standard sliding windows fail because shrinking the left pointer might preserve validity while skipping hidden matching sub-segments.
* Core Insight:
  Finding subarrays with *exactly* $k$ distinct elements is exceptionally difficult with a single sliding window because moving the left pointer can alter unique counts unpredictably. However, calculating subarrays with *at most* $k$ distinct elements is incredibly simple: on each step, adding `right - left + 1` adds the count of all valid subarrays ending at the current right pointer. Because the set of subarrays with exactly $k$ distinct elements equals (subarrays with at most k distinct) − (subarrays with at most k−1 distinct), computing `atMost(k) - atMost(k - 1)` isolates the exact matches in linear time.
* Mistakes made: The ultimate cognitive challenge was figuring out how to handle the "exact match" constraint without introducing an inner re-scan loop. Discovering that a dynamic sliding window naturally counts *ranges* of subarrays via prefix totals (`ans += right - left + 1`), and learning to use mathematical subtraction to isolate exact counts was the most advanced thought-driven breakthrough of the series.
* What I learned: Complex exact-count sliding constraints can be solved by combining simpler inequality ranges mathematically. Tracking the absolute index difference `(right - left + 1)` during an expandable sweep accumulates valid sub-ranges automatically, turning a tricky tracking problem into a clean, linear calculation sequence.