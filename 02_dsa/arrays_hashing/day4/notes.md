## Problem: Top K Frequent Elements

* Brute force: Counting frequencies with a Counter, converting it to a standard dictionary, and running a loop 'K' times that performs an expensive linear scan to find, append, and pop the maximum frequency element.
```python
from collections import Counter
def top_k_frequent(nums, k):
    output_list = []
    nums_counter = dict(Counter(nums))
    for i in range(1, k + 1):
        freq = max(nums_counter, key=nums_counter.get)
        output_list.append(freq)
        nums_counter.pop(freq) 
    return output_list    
```
* Optimized: Using Bucket Sort by grouping unique numbers into a bucket array where index i stores all numbers appearing exactly i times, then traversing the buckets backward to collect the top 'K' items.
```python
from collections import Counter

def top_k_frequent_optimized(nums, k):
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    
    for num, frequency in counts.items():
        buckets[frequency].append(num)
        
    output_list = []
    for i in range(len(buckets) - 1, 0, -1):
        for num in buckets[i]:
            output_list.append(num)
            if len(output_list) == k:
                return output_list
```
* Data structure used: Standard Dictionary (`dict`) and linear list lookups for brute force; Hash Map combined with an Array of Lists (`list[list]`) for optimization.
* Complexity:
  * Brute Force: Time O(N + K × M) where 'M' is unique elements (Worst-case O(K × N) if all items are unique); Space O(M) where M is the number of unique elements (worst case O(N)).
  * Optimized: Time (O(N)) for single-pass bucketing and gathering; Space O(N) for the bucket array plus frequency storage.
* Mistakes made: Hardcoding a fixed integer limit into frequency extraction parameters originally instead of evaluating the dynamic input variable `k`.
* What I learned: Relying on `.pop()` removes dictionary keys successfully, but extracting the maximum element inside a loop using `max(..., key=dict.get)` forces an (O(M)) linear scan on every single iteration. More importantly, I learned how Python handles nested mutable objects: using pointer replication like `[[]] * (n + 1)` creates a massive trap where all indices reference one shared list object in memory, meaning mutating a single slot updates every single row simultaneously. Using a proper list comprehension `[[] for _ in range(n + 1)]` is mandatory because it creates a distinct, isolated list object per iteration.

---

## Problem: Valid Sudoku

* Best Practical Solution: Creating 27 independent hash sets (9 for rows, 9 for columns, and 9 for 3x3 grids) and manually verifying membership for each cell to identify board duplication errors.
```python
def is_valid_sudoku_sets(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == ".":
                continue
                
            box_idx = (r // 3) * 3 + (c // 3)
            if val in rows[r] or val in cols[c] or val in boxes[box_idx]:
                return False
                
            rows[r].add(val)
            cols[c].add(val)
            boxes[box_idx].add(val)
    return True
```
* Alternative Hash Signature Approach: Using a single pass over the board with one tracking Counter by transforming row, column, and sub-grid validation criteria into unique descriptive text strings.
```python
from collections import Counter

def is_valid_sudoku(board):
    sudoku_counter = Counter()
    for row in range(9):
        for col in range(9):
            val = board[row][col]
            if val == ".":
                continue
            row_key = f"{val} in row {row}"
            col_key = f"{val} in col {col}"
            grid_key = f"{val} in grid {row // 3}-{col // 3}"
            
            sudoku_counter[row_key] += 1
            sudoku_counter[col_key] += 1
            sudoku_counter[grid_key] += 1
            
            if (sudoku_counter[row_key] > 1 or 
                sudoku_counter[col_key] > 1 or 
                sudoku_counter[grid_key] > 1): 
                return False
    return True
```
* Data structure used: An array of 27 separate hash sets (`list[set]`) for best practical solution; One flat Hash Map bag structure (`collections.Counter`) for alternative hash signature approach.
* Complexity:
  * Time O(N^2) for an N×N board; for standard Sudoku this becomes O(1) since N = 9 is fixed.
  * Space O(N^2) in the generalized N×N Sudoku case because row, column, and box trackers collectively may store up to O(N^2) entries; for standard Sudoku this simplifies to O(1).
* Mistakes made: 
  1. Omitting explicit spatial qualifiers like "row" or "col" in the string formatting template (`f"{val} in {row}"`). This caused an immediate self-collision on cross-diagonal intersection cells (like row 0, column 0), where both formulas computed an identical string signature and falsely triggered duplicate detection flags.
  2. Confusing shared references with recursive references during debugging. Structures created using pointer replication (like nested mutable containers built incorrectly) can behave unexpectedly because multiple locations may point to the same object in memory. This reinforced the importance of understanding aliasing vs true circular references.
* What I learned: Dictionary key schemas must enforce absolute domain isolation to prevent accidental namespace cross-contamination. I also learned that using floor division arithmetic `row // 3` successfully compresses an expansive grid into distinct operational coordinate IDs. Most importantly, recursive displays like {...} or [...] usually indicate Python detected a circular self-reference during printing, while repeated unexpected updates across nested containers often indicate shared references (aliasing). These are related but different bugs.

---

## Problem: Encode and Decode Strings

* Brute force: Attempting to use a dictionary comprehension to store string-to-length maps, before serializing them into a single string with a length-and-hash delimiter format.
```python
def encode_brute(strs):
    encode_dict = {string: len(string) for string in strs}
    encode_str = ""
    for word, length in encode_dict.items():
        encode_str += f"{length}#{word}"
    return encode_str
```
* Optimized: Iterating through the raw list directly to build length-prefixed chunks concatenated via an array join, and decoding the flat string via dynamic index jump pointers.
```python
def encode(strs):
    encoded_pieces = []
    for word in strs:
        encoded_pieces.append(f"{len(word)}#{word}")
    return "".join(encoded_pieces)

def decode(s):
    decode_list = []
    i = 0
    while i < len(s):
        j = i
        while s[j] != "#":
            j += 1
        length = int(s[i:j])
        word = s[j + 1 : j + 1 + length]
        decode_list.append(word)
        i = j + 1 + length
    return decode_list
```
* Data structure used: Dictionary comprehension (`dict`) for brute force; Python Lists (`list`) and while-loop character markers for optimization.
* Complexity:
  * Brute Force: Time O(N^2) in the worst case because repeated string concatenation inside a loop causes repeated copying of previously built content; Space O(M) for unique strings map (excluding concatenation overhead).
  * Optimized: Time O(N), where N is total number of characters across all strings plus delimiter/length metadata; Space O(N) for storage blocks.
* Mistakes made: Using a dictionary comprehension (`encode_dict = {string: len(string) for string in strs}`) to isolate list elements. Because dictionary keys must be unique, any duplicate strings in the input list (e.g., `["a", "a", "a"]`) would overwrite each other, causing data loss and rendering the code incapable of decoding back into the original array. For the decoding logic, attempting a `for` loop slice with static increments failed because it didn't account for multi-digit lengths or variable index shifting.
* What I learned: Encoding-decoding architectures must guarantee that `decode(encode(strs)) == strs`. Transforming input lists into tracking dictionaries strips away matching structural frequencies. Using a `while` loop with variable pointer adjustments allows you to read boundary integers dynamically, safeguarding the mechanism against inner character delimiters like embedded hash symbols.
