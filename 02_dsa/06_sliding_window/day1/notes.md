## Problem: Best Time to Buy and Sell Stock

* Brute force: Using nested loops to evaluate every possible pairing of buy days and subsequent sell days, computing the difference for each pair to find the maximum profit.
```python
def best_time_stock_brute(prices):
    max_profit = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            profit = prices[j] - prices[i]
            max_profit = max(max_profit, profit)
    return max_profit
```
* Optimized: Running a sliding window pointer system where the left pointer tracks the absolute lowest buying price seen so far and the right pointer advances daily to compute and maximize rolling profit margins.
```python
def best_time_stock(prices):
    buy = 0 
    sell = 1  
    max_profit = 0
    while sell < len(prices):
        if prices[buy] < prices[sell]:
            current_profit = prices[sell] - prices[buy]
            max_profit = max(max_profit, current_profit)
        else:
            buy = sell
        sell += 1
    return max_profit
```
* Data structure used: None; primitive boundary tracker index pointers (`buy`, `sell`) are manipulated directly.
* Complexity:
  * Brute Force: Time $O(n^2)$ due to nested loop pairings over historical arrays; Space $O(1)$.
  * Optimized: Time $O(n)$ for a single linear sweep across price milestones; Space $O(1)$ constant auxiliary memory.
* Pattern Recognition:
  * Use running-state optimization / two-pointer style when:
    - You need to track an extreme boundary (like a historical best) while looking forward at upcoming options.
    - Shifting your boundary point to a newly discovered optimal asset position instantly invalidates all intermediate elements. Current answer depends on past extreme + current value
* Core Insight:
  You can never make a profit by selling on a day that comes before you buy. Instead of comparing all future combinations, the moment you discover a selling price cheaper than your current buy day (`prices[sell] < prices[buy]`), that sell day automatically becomes your optimal new entry floor, allowing you to slide your buy pointer directly to it.
* Mistakes made: None. Independently structured the window shortcut `buy = sell` which completely bypassed the need to step the left pointer through the array indices one-by-one.
* What I learned: Keeping state tracking variables anchored to relative boundaries eliminates redundant historical scans. The sliding window pattern turns a complex chronological comparison problem into a smooth single-pass tracking routine.

---

## Problem: Longest Substring Without Repeating Characters

* Brute force: Generating every possible contiguous substring window from the string using nested loops, and running a character validation check on each substring to confirm it contains zero duplicate letters.
```python
def substring_brute(s):
    max_len = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            window = s[i:j]
            if len(set(window)) == len(window):
                max_len = max(max_len, j - i)
    return max_len
```
* Optimized: Driving a linear sliding window pass across the string where a hash map tracks the last seen index of every character, allowing the left pointer to instantly snap forward past duplicate elements without any index backtracking.
```python
def substring_longest(s):
    char_map = {}
    first = 0
    max_length = 0
    for second in range(len(s)):
        if s[second] in char_map and char_map[s[second]] >= first:
            first = char_map[s[second]] + 1
        char_map[s[second]] = second
        max_length = max(max_length, second - first + 1)
    return max_length
```
* Data structure used: Slice membership evaluation for brute force; Hash Map / Dictionary (`dict`) mapping `{char: int}` to track recent character positions for optimization.
* Complexity:
  * Brute Force: Time $O(n^3)$ due to nesting substring windows combined with inner set constructions; Space $O(n)$.
  * Optimized: Time $O(n)$ because both the left and right pointers sweep across characters without manual backtracking loops; Space $O(m)$ where $m$ is the number of unique characters in the string alphabet.
* Pattern Recognition:
  * Use a sliding window hash map when:
    - You need to track contiguous ranges or sub-segments that match uniqueness constraints.
    - Re-evaluating past window segments character by character creates an expensive processing bottleneck.
* Core Insight:
  When a duplicate character enters the right side of the window, you do not need to slide your left pointer forward step-by-step or rewind your right pointer. A hash map tells you the exact index where that duplicate was last seen, allowing you to instantly snap the left wall right past it (`first = char_map[s[second]] + 1`) to reset a clean, non-repeating sub-segment.
* Mistakes made: Initial difficulty was implementing a list slice membership check (`s[second] not in s[first:second]`), which introduced an expensive hidden linear scan on every loop pass, elevating the algorithm's time complexity to a slow quadratic rate. Furthermore, attempting to manage collisions by decrementing the right pointer pointer (`second -= 1`) created a bug-prone backtracking state that re-evaluated identical elements repeatedly and risked entering infinite loops on certain characters.
* What I learned: Character tracking slices create secret performance drains inside loop routines. Mapping positions inside a dictionary gives immediate constant-time index lookups, turning a chaotic pointer-manipulation routine into a sleek single-pass operation.