## Problem: Combination Sum II

* **Problem Type:** Duplicate Pruning Backtracking / Single-Use Constrained DFS
* **Data Structure Used:** Sorted Array + State Buffer Array (`list`)
* **Approach 1:** Loop-Based Combination Search. Iterate across candidate indices using a standard loop range, inserting a duplicate lookahead check (`if i > start and candidates[i] == candidates[i-1]: continue`) right inside the loop header to skip repetitive values. While optimal, it shifts structural tracking away from a pure binary choice representation.
* **Optimized Approach:** Binary Choice Backtracking (Include/Exclude Framework) with Post-Inversion Duplicate Throttling. Sort the dataset up front to anchor identical values in contiguous memory blocks. The inclusion track steps forward normally while advancing the index (`dfs(i + 1, current_total + candidates[i])`). Upon rolling back (`combination.pop()`), a fast lookahead `while` loop advances the pointer past all identical sibling characters before launching the exclusion track (`dfs(i + 1, current_total)`), pruning identical choice paths completely.
* **Complexity:**
  * **Time:** Exponential (worst case approximately $O(2^n)$ after sorting)
    - Why $O(2^n)$? because every element faces a binary inclusion or exclusion decision step, though real-world execution frames are cut down drastically by the duplicate pruning filter.
  * **Space:** $O(n)$ to handle the maximum depth allocation bounds of the recursive call stack.
* **Pointer Flow:**
```text
Duplicate pruning tree forks:
dfs(0,0)
├── Include 1
│   └── dfs(1,1)
│       ├── Include 1
│       │   └── dfs(2,2)
│       │       ...
│       └── Exclude 1
│           └── Skip duplicate 1
│               └── dfs(2,1)
└── Exclude 1
    └── Skip duplicate 1
        └── dfs(2,0)
```
* **Pattern Recognition:**
  * Use a binary include-exclude duplicate pruning layout when:
    - Elements must be used at most once per combination track.
    - The candidate array contains duplicated items, but the final output collection demands strictly unique sets.
* **Core Insight:** This problem perfectly bridges **Combination Sum** and **Subsets II**. By enforcing a strict single-use tracking step (`i + 1`) on the inclusion track and leveraging a post-inversion `while` filter on the exclusion track, the algorithm isolates unique combinations across duplicated numbers without requiring external set structures.
* **Mistakes Made:** The primary conceptual trap was misinterpreting the array limits inside the lookahead skip check. Forgetting to use a local pointer threshold boundary validation (`i + 1 < len(candidates)`) causes the index shifter to throw an out-of-bounds crash when identical duplicate elements reside right at the terminal end of the input list.
* **What I Learned:** Combining sort blocks with trailing pointer throttling handles single-use duplicate constraints cleanly. It turns a risky permutational tree into a well-behaved linear search path.

---

## Problem: Combinations

* **Problem Type:** Size-Capped Combinatorial Selection / Choice Range DFS
* **Data Structure Used:** Flat Choice Stack (`list`)
* **Approach 1:** Include/Exclude Binary Split. Mapping the problem space to a series of $n$ pick/skip choices, tracking the index layer manually. While functional, it requires managing dual tracking exit states (both length checks and range exhausts) concurrently.
* **Optimized Approach:** Loop-Driven Range Backtracking. Iterate from a progressive tracking anchor (`start`) up to the boundary limit $n$. On each step, push the digit onto your stack, recurse forward with a strictly incremented parameter (`i + 1`) to prevent self-duplication, and pop the element on the way back up to restore the previous state. Exit the frame the exact moment the stack length matches the target cap (`len(combination) == k`).
* **Complexity:**
  * **Time:** $O(k \cdot \binom{n}{k})$ where $\binom{n}{k}$ is the binomial coefficient tracking total valid combinations, multiplied by the $O(k)$ array cloning footprint.
  * **Space:** $O(k)$ auxiliary space memory bounded by the maximum stack depth allocation.
* **Pointer Flow:**
```text
Loop range choice tree steps:
dfs(1)
├── Pick 1
│   └── dfs(2)
│       ├── Pick 2 -> [1,2]
│       ├── Pick 3 -> [1,3]
│       └── Pick 4 -> [1,4]
├── Pick 2
│   └── dfs(3)
│       ├── Pick 3 -> [2,3]
│       └── Pick 4 -> [2,4]
├── Pick 3
│   └── dfs(4)
│       └── Pick 4 -> [3,4]
└── Pick 4
```
* **Pattern Recognition:**
  * Use loop-driven range backtracking when:
    - The problem asks for combinations of an exact size constraint $k$ derived from a continuous, monotonically increasing value range.
    - Element ordering does not matter (e.g., [1,2] is identical to [2,1]), meaning you only ever look forward.
* **Core Insight:** Range loops naturally enforce combinatorial tracking order. By forcing the internal loop step to inherit a progressive baseline pointer (`i + 1`), the algorithm permanently locks out lower integers behind it, which naturally blocks duplicate inverse permutations without needing high-overhead storage tables.
* **Mistakes Made:** The thought-driven bottleneck was handling the upper range boundary cleanly. Ensuring that the loop extends inclusively to evaluate the target ceiling (`range(start, n + 1)`) takes strict boundary care; an off-by-one error here will silently truncate your search space, causing your outputs to completely miss combinations containing the final digit $n$.
* **What I Learned:** Progressive loop thresholds eliminate reverse duplicate tracking paths automatically. Keeping exit gates locked to stack lengths ensures that only perfectly formed combinations are cached into your results.

---

## Problem: Permutations

* **Problem Type:** Array-Swapping Permutational DFS / Complete Choice Exhaustion
* **Data Structure Used:** In-Place Mutating Array (`list`)
* **Approach 1:** Visited Map Tracking. Maintaining a secondary boolean array or hash set (`visited = set()`) to track which elements are currently locked inside the path stack, loop-scanning all candidates on every layer, and skipping already active entries. This works cleanly but requires an $O(n)$ auxiliary memory buffer to track state history continuously.
* **Optimized Approach:** In-Place Pointer Swapping Backtracking. Drive a recursive tree that tracks an active focus position index `start`. Loop a cursor `i` from `start` to the end of the array, swapping the elements in place (`nums[start], nums[i] = nums[i], nums[start]`) to place a new candidate at the active focus slot. Recurse forward to process the next position (`start + 1`), and execute an identical mirror swap right after to rollback the modification and restore original state contexts for sibling branches.
* **Complexity:**
  * **Time:** $O(n \cdot n!)$ because a set of size $n$ possesses exactly $n!$ unique permutations, and cloning each layout array into results costs $O(n)$ time operations.
  * **Space:** $O(n)$ auxiliary memory space corresponding to the depth of the recursive call stack.
* **Pointer Flow:**
```text
In-place memory swapping tree tracks:
[1,2,3]

start=0

Swap(0,0)
├── [1,2,3]
│   ├── Swap(1,1)
│   │   └── [1,2,3]
│   └── Swap(1,2)
│       └── [1,3,2]

Swap(0,1)
├── [2,1,3]
│   ├── ...
```
* **Pattern Recognition:**
  * Use in-place pointer swapping when:
    - The goal requires generating *every single possible ordering* of a fixed collection of elements where sequence placement matters (e.g., [1,2,3] and [1,3,2] are both unique, mandatory solutions).
    - You want to eliminate the memory overhead of secondary visited sets or path buffers entirely.
* **Core Insight:** Permutations require exploring every possible layout variant. By partitioning the array into a fixed, solved prefix region (everything before `start`) and an open, active choice region (everything from `start` onwards), swapping elements directly inside the input array allows you to evaluate every permutation branch without allocating any extra list space on the heap.
* **Mistakes Made:** The primary conceptual trap was misinterpreting the recursive propagation step. Advancing the call stack using the loop cursor index (`dfs(i + 1)`) instead of the focus pointer index (`dfs(start + 1)`) breaks the tree entirely, forcing the pointer to skip active tracking frames and resulting in a corrupted collection of truncated or duplicated layouts.
* **What I Learned:** Swapping elements in place is an incredibly elegant way to handle permutations without memory overhead. It converts a complex ordering task into a balanced sequence of forward mutations and precise historical rollbacks.

---

## Problem: Permutations II

* **Problem Type:** Deduplicated Permutational Backtracking / Frequency Map Choice Tree
* **Data Structure Used:** Frequency Hash Map + State Buffer Stack (`dict` + `list`)
* **Approach 1:** Sorted Swap Pruning. Sorting the input array up front and utilizing the in-place pointer swapping approach, while inserting complex lookahead neighborhood conditionals to block duplicate values at the same level. This is highly difficult to implement accurately due to elements shifting positions dynamically across swap frames.
* **Optimized Approach:** Frequency Map Backtracking. Flatten the input array into a compiled frequency hash table (`count`) up front, recording the unique count of each digit. Drive a loop that iterates exclusively over the *unique keys* of the frequency map. If a key has an available count greater than 0, push it onto your permutation stack, decrement its count balance, recurse forward, and increment the count back alongside a stack pop on the way up.
* **Complexity:**
  * **Time:** $O(n \cdot n!)$ worst-case allocations, but performs significantly fewer recursive calls when many duplicate values exist because only unique keys are explored at each level.
  * **Space:** $O(n)$ space allocations to manage the unique key frequency map balances and stack frames.
* **Pointer Flow:**
```text
Frequency map tree selections:
                               dfs()
                         /              \
                  Pick Key 1          Pick Key 2
               count={1:1, 2:1}    count={1:2, 2:0}
                   Perm:                    Perm:
                 /       \                    |
           Pick Key 1      Pick Key 2     Pick Key 1 (Only option left)
        count={1:0,2:1}  count={1:1,2:0}
           Perm:     Perm:  Perm:
```
* **Pattern Recognition:**
  * Use a frequency map choice tree when:
    - The problem demands generating all unique orderings (permutations) of a collection that contains heavily duplicated or repetitive numbers.
    - Standard swapping patterns fail because identical elements at different array index slots create duplicate search paths.
* **Core Insight:** Duplication in permutations occurs when you attempt to place the exact same value into the same relative slot position multiple times across sibling branches. By looping strictly over the *unique keys* of a frequency map instead of raw index lines, you guarantee that each distinct number is evaluated at that slot position exactly once, completely preventing duplicate paths from ever opening.
* **Mistakes Made:** The primary thought-driven hurdle was breaking the habit of using an index-based tracking pointer (`start_index`) inside the recursive signature. Realizing that a permutation check cares about *global item availability* rather than forward index restrictions was the key breakthrough; the frequency map inherently acts as your global availability compass, meaning the recursive call can execute completely parameter-free (`dfs()`).
* **What I Learned:** Decoupling choice tracks from raw list arrays via frequency tables eliminates duplicate permutations cleanly. It preserves strict linear memory limits while automatically pruning identical branches before they can execute.

---

## Problem: Letter Combinations of a Phone Keypad

* **Problem Type:** Cartesian Product Generation / Keypad Mapping DFS
* **Data Structure Used:** Constant Direct-Address Hash Map + String String Builder (`dict` + `str`)
* **Approach 1:** N/A
* **Optimized Approach:** Establish a static, pre-allocated lookup dictionary mapping keypad digits to their matching character blocks. Drive a top-down recursive DFS pass that takes an active string index pointer `i` and a running text string accumulator `current_str`. In each frame, access the specific character group mapped to the digit `digits[i]`, loop through its letters, and propagate the track forward by executing a string concatenation step directly inside the argument field (`dfs(i + 1, current_str + char)`).
* **Complexity:**
  * **Time:** $O(n \cdot 4^n)$ where $n$ is the total count of input digits, reflecting the maximum possible multi-branch split configurations triggered by keys like 7 and 9 (which contain 4 characters).
  * **Space:** $O(n)$ space complexity required to house the recursive call frames on the execution stack.
* **Pointer Flow:**
```text
Cartesian path expansions for digits = "23" -> Mapping {"2": "abc", "3": "def"}:
                         dfs(i=0, current_str="")
                    /               |               \
              char='a'           char='b'           char='c'
             dfs(1, "a")        dfs(1, "b")        dfs(1, "c")
             /   |   \
      char='d'  'e'   'f'
          /      |     \
       "ad"    "ae"    "af" (All hit len == 2; Saved!)
```
* **Pattern Recognition:**
  * Use a keypad mapping Cartesian DFS when:
    - The problem requires tracking all possible string combinations generated by character clusters mapped to independent sequential tokens.
    - Every selection track forms a fixed, balanced path whose final length matches the input array length exactly.
* **Core Insight:** This problem represents a pure Cartesian Product expansion track. Because the character groups belong to separate, independent digits, you never need to worry about item lookup exclusions or element sorting. Simply pass the newly formed string copy directly into the recursive argument field (`current_str + char`); because strings are immutable values in Python, this automatically isolates path memory, completely bypassing the need to write an explicit `.pop()` rollback step.
* **Mistakes Made:** The hardest thought-driven hurdle was managing empty inputs cleanly. If the input string is blank (`digits = ""`), a naive recursive parser will immediately output an invalid list containing an empty string (`[""]`) instead of a completely empty list (`[]`). Placing an explicit fast-fail guard condition right at the front of the function (`if not digits: return []`) protects the entry boundary against this edge case.
* **What I Learned:** Value argument passing handles backtracking tracking states cleanly on immutable types. Leveraging string parameters removes explicit rollback commands, keeping combinatorial pipelines exceptionally clean and fast.

---

### Comparison Table

| Problem | Tree Architecture | Element Reuse Rule | Duplicate Management | Loop Structure | Base Case Constraint |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Subsets** | Binary Include / Exclude | Single-Use ($i + 1$) | N/A (Unique inputs) | No loops | $i \ge \text{len(nums)}$ |
| **Subsets II** | Binary Include / Exclude | Single-Use ($i + 1$) | Contiguous Sort + Exclusion Pointer Throttle | Loop inside Exclusion | $i \ge \text{len(nums)}$ |
| **Combination Sum** | Binary Include / Exclude | Unbounded / Infinite ($i$) | N/A (Unique inputs) | No loops | $\text{total} == \text{target}$ (Success)<br>$\text{total} > \text{target}$ (Prune) |
| **Combination Sum II** | Binary Include / Exclude | Single-Use ($i + 1$) | Contiguous Sort + Exclusion Pointer Throttle | Loop inside Exclusion | $\text{total} == \text{target}$ (Success)<br>$\text{total} > \text{target}$ (Prune) |
| **Combinations** | Loop-Driven Progressive Range | Single-Use ($i + 1$) | N/A (Unique range) | Forward loop (`start` to $n$) | $\text{len(buffer)} == k$ |
| **Permutations** | In-Place Memory Swapping | Single-Use ($start + 1$) | N/A (Unique inputs) | Forward loop (`start` to end) | $start == \text{len(nums)}$ |
| **Permutations II** | Frequency Map Choice Tree | Limited by Frequency | Unique Key Extraction via Hash Map | Map Key Iteration loop | $\text{len(buffer)} == \text{len(nums)}$ |
| **Letter Combinations** | Cartesian Product Expansion | Single-Use ($i + 1$) | N/A (Distinct digit blocks) | Mapped string token loop | $\text{len(buffer)} == \text{len(digits)}$ |

---

### Master Patterns Learned

#### 1. In-Place Structural Permuting (The Memory-Zero Swap Frame)
* **Applied to:** Permutations
* **The Strategy:** Use this architectural blueprint when a problem requires generating every possible structural configuration or ordering of a dataset where sequence placement matters, and you want to completely eliminate the memory footprint of secondary tracking maps or path arrays. Partition your list array directly into a static solved prefix zone and an active choice zone, swapping elements in place to validate variants cleanly.
* **The Conceptual Mechanics:**
  - **Memory Space Virtualization:** Instead of allocating memory for a dedicated sub-list or tracking state on the heap, you use the input array itself as your primary workspace. The focus index pointer (`start`) acts as a clear boundary wall: everything behind it is locked down, and everything in front represents available option cards you can swap into place.
  - **Symmetric Balance Restoration:** Modifying global reference buffers in place requires strict execution symmetry. For every forward mutation swap you execute to launch a recursive branch, you must run an identical twin swap right after the stack unrolls to erase your footprints, preserving structural integrity for alternative lanes.
* **The Layout / Code Pattern:**
```python
def generate_zero_space_permutations(nums: list) -> list:
    results = []
    
    def permute_core(start):
        # Base Case: All index slots configured -> Capture current array layout snapshot
        if start == len(nums):
            results.append(list(nums))          # Deep copy the current layout state
            return
            
        for i in range(start, len(nums)):
            # Choose: Swap the candidate item into the active focus slot
            nums[start], nums[i] = nums[i], nums[start]
            
            # Explore: Advance focus pointer to configure the next slot down the line
            permute_core(start + 1)
            
            # Undo: Reverse the swap to restore memory context for sibling options
            nums[start], nums[i] = nums[i], nums[start]
            
    permute_core(0)
    return results
```
* **Recognition Signals / Triggers:**
  - Structural keywords like **"Arrange"**, **"Ordering"**, or **"Every unique ordering / arrangement"**.
  - Context indicators where element position explicitly dictates solution uniqueness (e.g., `[1, 2]` is treated differently from `[2, 1]`).
  - Imposed system constraints requiring you to **use each element exactly once** per branch track layout.

#### 2. Unique Key Frequency Mapping (The Permutational Deduplicator)
* **Applied to:** Permutations II
* **The Strategy:** Use this pattern when you need to calculate orderings or permutations over an array that contains heavily duplicated or repetitive data fields. Standard index swapping rules fail here because identical items at different array index slots create identical choice branches. Bypassing this problem is achieved by flattening the array into a frequency hash map up front, forcing the backtracking loop to iterate exclusively across the *unique keys* of the map.
* **The Conceptual Mechanics:**
  - **Unique Placement Enforcement:** Duplication happens when you try to place the exact same value into the same relative slot position multiple times across sibling tracks. Iterating over the unique keys of a frequency dictionary ensures each distinct integer value gets a shot at that slot position exactly once.
  - **Global Inventory Tracking:** Because choice tracks are decoupled from local forward-moving indices, availability is checked by reading the map's count registers (`count[key] > 0`). This allows the recursive tracker to clear its parameter signature entirely (`dfs()`), relying on the map as an absolute inventory compass.
* **The Layout / Code Pattern:**
```python
import collections

def deduplicated_permutations(nums: list) -> list:
    results = []
    buffer_stack = []
    # Step 1: Flatten input into a unique key density blueprint
    frequency_map = collections.Counter(nums)
    
    def discover_orderings():
        if len(buffer_stack) == len(nums):
            results.append(list(buffer_stack))
            return
            
        # Loop strictly across UNIQUE keys to block duplicate sibling lanes
        for unique_item in frequency_map:
            if frequency_map[unique_item] > 0:
                # Choose
                buffer_stack.append(unique_item)
                frequency_map[unique_item] -= 1
                
                # Explore (Parameter-free: relies on global inventory balances)
                discover_orderings()
                
                # Undo
                frequency_map[unique_item] += 1
                buffer_stack.pop()
                
    discover_orderings()
    return results
```
* **Recognition Signals / Triggers:**
  - Structural demands stating **"Unique permutations"**, **"Distinct layout orderings"**, or **"No duplicate arrangements"**.
  - Input arrays characterized by containing heavily **duplicated/repetitive components**.
  - Constraints where sequence positions matter, yet standard sorting or swapping boundaries fall short.

#### 3. Cartesian Immutable Value Passing (The Pop-Less Multi-Group Combiner)
* **Applied to:** Letter Combinations of a Phone Keypad
* **The Strategy:** Use this architectural framework when your system must compile all possible combination variants (the Cartesian Product) across multiple independent, isolated token groups (like keypad letters, character matrices, or attribute maps). Instead of driving heavy state array allocations that require an explicit `.pop()` rollback step, pass string accumulations straight inside the recursive argument field to isolate path context automatically.
* **The Conceptual Mechanics:**
  - **Automatic Context Isolation:** In Python, strings are immutable values passed by copy buffer references. Appending a character directly inside the functional argument line (`current_str + char`) spawns a unique string instance exclusive to that specific downstream recursive frame, completely removing the need to manage manual array cleanups or pops.
  - **Independent Group Hopping:** Because option blocks belong to separate standalone inputs (e.g., button 2 has keys 'abc', button 3 has keys 'def'), items never compete for availability. Pointers move forward across groups via a flat single index step (`i + 1`), creating a perfectly balanced combination tree.
* **The Layout / Code Pattern:**
```python
def generate_cartesian_combinations(token_sequence: str, token_attribute_map: dict) -> list:
    if not token_sequence:
        return []       # Fast-fail boundary guard condition
        
    global_combinations = []
    
    def process_group(group_index, accumulated_string):
        # Base Case: Reached terminal boundary (All groups visited)
        if group_index == len(token_sequence):
            global_combinations.append(accumulated_string)
            return
            
        # Target active token cluster layout
        active_token = token_sequence[group_index]
        available_choices = token_attribute_map[active_token]
        
        for choice in available_choices:
            # Explore + Choose concurrently inside the argument pipeline
            # Immutable value cloning completely eliminates the need for a trailing pop step!
            process_group(group_index + 1, accumulated_string + choice)
            
    process_group(0, "")
    return global_combinations
```
* **Recognition Signals / Triggers:**
  - System prompts requesting to **"Generate strings from groups"** or combine elements from disjoint **"token clusters / maps"**.
  - Direct problem context clues like **"Keypad mapping"**, **"Combination dial"**, or computing a raw cross-product sequence.
  - Combinatorial trees requiring you to **choose exactly 1 option per group**, creating path arrays whose length directly corresponds to the query length.