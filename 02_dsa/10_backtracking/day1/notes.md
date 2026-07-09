# Backtracking

## What is Backtracking?

Backtracking is a systematic algorithmic paradigm used to find solutions to computational problems by exploring a multi-branch search space step-by-step. It incrementally builds candidates toward a solution and abandons a path ("backtracks") as soon as it determines the current path cannot satisfy the constraints. Essentially, it acts as a controlled Depth-First Search (DFS) over an implicit **Decision Tree**, where each node represents a choice point and each branch represents a potential branch lane.

---

## Generic Backtracking Template

```python
def solve_problem(inputs):
    result = []
    state_buffer = []       # Tracks the current path or candidate choice combination
    
    def backtrack(start_index):
        # 1. BASE CASE / GOAL CHECK: If the target boundary condition is reached
        if is_solution(state_buffer):
            result.append(list(state_buffer))       # Deep copy the snapshot buffer
            return
            
        # 2. EXPLORE DECISION SPACE: Iterate through all available candidates
        for i in range(start_index, len(inputs)):
            candidate = inputs[i]
            
            # Prune invalid paths early using constraint filtering
            if not is_valid(candidate, state_buffer):
                continue        # Skip dead ends
                
            # 3. CHOOSE: Commit to the candidate and mutate state
            state_buffer.append(candidate)
            
            # 4. EXPLORE: Recurse deeper into the decision tree branch (arguments depend on the problem)
            backtrack(i + 1)          # Adjust recursive state based on the problem (index, remaining target, visited set, etc.)
            
            # 5. UNDO: Rollback the decision to restore context for the next sibling branch
            state_buffer.pop()
            
    backtrack(0)
    return result
```

### Generic Complexity

Worst-case complexity depends on the branching factor and recursion depth.

For most backtracking problems:

* Time: Usually exponential (depends on branching factor)
* Space: O(depth of recursion)

Backtracking intentionally explores many possibilities, but pruning can significantly reduce the practical runtime.

---

## Choose → Explore → Undo

The heartbeat of any backtracking routine rests on three synchronized steps:
* **Choose**: You pick a valid candidate from the current node's option pool and append it to your state buffer. This mutates your running context and marks a step forward down a specific search path.
* **Explore**: You fire off a recursive call to dive deeper into the decision tree, processing downstream subproblems under the assumption that your previous choice was correct.
* **Undo**: The absolute moment the recursive path hits a base case or a dead end and winds back up, you must explicitly pop the candidate out of your state buffer. This cleans up the global tracking registers and restores the exact context needed for the next sibling branch to be evaluated safely.

---

## Decision Tree

Every backtracking problem can be visualized as a structured **Decision Tree**. 
* **The Root Node** represents your blank initial state (an empty list, an empty string, or your starting coordinates).
* **The Edges/Branches** represent individual choices made at that point in time.
* **The Leaf Nodes** represent either a dead end (pruned by constraint checks) or a valid solution boundary (appended to your final results).

Visualizing the tree helps you calculate exactly how your indices transition and where you can introduce aggressive **pruning filters** to cut off whole sections of the search space before wasting processing steps on a dead end.

---

## Characteristics of Backtracking

Backtracking problems generally have the following characteristics:

* Multiple choices exist at each step.
* A partial solution can be built incrementally.
* Invalid paths can be detected before reaching a complete solution.
* The algorithm must explore every valid possibility (unless pruning removes branches).
* State changes must always be reversible.
* Solutions are typically generated using recursion.

Common examples include:

* Subsets
* Permutations
* Combinations
* N-Queens
* Sudoku Solver
* Word Search
* Palindrome Partitioning

---

## Pruning

Pruning is the process of terminating a recursive branch as early as possible because it can no longer produce a valid solution.

Instead of exploring an impossible subtree, we immediately return.

Examples:

* Current sum exceeds target.
* Index goes out of bounds.
* Duplicate branch detected.
* Constraint violated.
* Cell already visited.

Good pruning dramatically reduces the search space while still preserving correctness.

---

## Problem: Subsets

* **Problem Type:** Binary Decision Tree Backtracking / Include-Exclude Paradigm
* **Data Structure Used:** State Buffer Array (`list`)
* **Approach 1:** Loop-Based Cascading Index. Run a recursive loop from a `start_index` to the end of the array, pushing elements onto a stack and appending a snapshot copy at the beginning of each frame. This generates subsets by moving forward sequentially, building the combinations through loop ranges.
* **Optimized Approach:** Binary Choice Backtracking (Include/Exclude Framework). Advance a single tracking cursor `i` from $0$ up to the length of the array. At each index, you force exactly two pure branching pathways: one branch where the current element is explicitly **included** (`subset.append(nums[i])`) followed by a step forward, and a second symmetric branch where the element is completely **excluded** (`subset.pop()`) followed by a step forward. Snapshot copies are saved exclusively when the pointer reaches the absolute terminal boundary of the tree ($i \ge \text{len(nums)}$).
* **Complexity:**
  * **Time:** $O(n \cdot 2^n)$
    - Why $O(n·2ⁿ)$? There are exactly $2ⁿ$ subsets. Each valid subset must be copied into the answer. Copying each subset costs $O(n)$ in the worst case.
  * **Space:** $O(n)$ space complexity mapping the maximum recursive height and call stack depth of the execution pipeline.
* **Pointer Flow:**
```text
Binary Include/Exclude Decision Tree:
                     []
                  /      \
              +1          -1
             /              \
          [1]               []
         /   \            /    \
      +2      -2        +2      -2
     /         \        /         \
 [1,2]         [1]    [2]          []
```
* **Pattern Recognition:**
  * Use a binary include-exclude traversal strategy when:
    - The problem structure maps to a collection of binary yes/no decisions across a fixed input array.
    - You want a clean, symmetric decision tree that processes element states explicitly without nesting horizontal loop indices.
* **Core Insight:** Every subset can be mathematically modeled as a binary vector where each element is either flipped "on" or "off". By driving a pure recursive split state that handles the inclusion path completely before executing an immediate rollback to fire the exclusion path, the tree naturally unrolls all $2^n$ combinations safely, guaranteeing you touch the terminal base case boundary with a uniquely formed subset array every single time.
* **Mistakes Made:** The primary thought-driven hurdle was understanding why we do not append snapshots continuously on every frame like a loop-based backtracking template does. In a pure binary include-exclude model, because the code does not use a loop to jump forward, saving snapshots prematurely results in redundant or intermediate duplicates. Forcing the save action to wait strictly until the cursor clears the array bounds ($i \ge \text{len(nums)}$) ensures that every leaf node represents an exact, fully evaluated unique path configuration.
* **What I Learned:** Binary choice trees turn backtracking into a clean conditional cascade. Splitting state logic cleanly between standalone inclusion and exclusion paths tracks complete tracking domains without shifting index bounds inside loop frameworks.

---

## Problem: Subsets II

* **Problem Type:** Duplicate Pruning Backtracking / Monotonic Constraint Skipping
* **Data Structure Used:** Sorted Array + State Buffer Array (`list`)
* **Approach 1:** Naive HashSet Filtering. Generating all possible subsets blindly using a standard combination tree, converting each resulting subset into a sorted tuple wrapper, and pushing them into a global tracking set (`set()`) to strip out duplicates before outputting. This works but forces a massive, wasteful performance drain due to fully exploring and allocating memory for duplicate branches that you are already guaranteed to throw away.
* **Optimized Approach:** Sort the input array up front to group identical numbers together. Run the standard binary include-exclude backtracking framework. The inclusion path proceeds normally. However, before firing the corresponding exclusion branch path, insert a tight **index throttling while-loop** (`while i + 1 < len(nums) and nums[i] == nums[i + 1]: i += 1`) that pushes the pointer past all adjacent identical integers. This effectively prunes the decision tree, skipping duplicate choices before they can ever spin up a new recursive call frame.
* **Complexity:**
  * **Time:** $O(n \cdot 2^n)$ overall, but pruning significantly reduces the number of recursive calls in practice.
  * **Space:** $O(n)$ auxiliary space to handle the depth of the recursive stack.
* **Pointer Flow:**
```text
Duplicate pruning tree transitions:
nums = [1,2,2] (Sorted)

                     dfs(0)
                        []
                     /      \
                 +1          -1
                /              \
             dfs(1)          dfs(1)
              [1]                []
             /   \             /   \
          +2      -2        +2     -2*
         /         |        /        |
      [1,2]    skip dup    [2]    skip dup
        |          |        |        |
       +2         dfs(3)   +2      dfs(3)
        |                   |
     [1,2,2]               [2,2]


* Before taking the exclusion branch, skip all adjacent duplicates.

while i+1 < len(nums) and nums[i] == nums[i+1]:
    i += 1
```
* **Pattern Recognition:**
  * Use a sorted skip constraint loop when:
    - The input array contains duplicated elements, but the final output collection demands strictly unique combinations.
    - You need to prune whole sub-branches of a decision tree at the same level to prevent duplicate tracking paths.
* **Core Insight:** If you choose to exclude a number (like the first `2` in `[1, 2, 2]`), choosing to include any subsequent identical `2` further down that same branch will result in an identical combination that has already been explored by previous inclusion tracks. Sorting the dataset turns duplicates into contiguous blocks, allowing a single lookahead condition to safely advance the cursor past the redundant options, maintaining unique results without external set filtering overhead.
* **Mistakes Made:** The thought-driven bottleneck was mastering the exact positioning of the duplicate throttling loop. Placing the `while` skip condition before the inclusion path completely breaks the algorithm, because it prevents the system from ever building subsets that contain multiple copies of the duplicate number legally (e.g., you would never discover `[2, 2]`). The skip logic must execute *after* the inclusion branch finishes and pops, explicitly guarding the exclusion track only.
* **What I Learned:** Sorting data enables clean lookahead boundary tracking. Throttling cursors on the exclusion line allows you to prune matching duplicate choice paths cleanly, preserving strict linear memory efficiency.

---

## Problem: Combination Sum

* **Problem Type:** Infinite-Reuse Decision Backtracking / Unbounded Knapsack Choice Tree
* **Data Structure Used:** State Buffer Array (`list`)
* **Approach 1:** N/A
* **Optimized Approach:** Deploy a binary include-exclude decision loop that accepts two tracking parameters: the current array pointer index `i` and a rolling sum accumulator `current_total`. To simulate **infinite reuse**, the inclusion branch path pushes the element to the stack but *does not increment the index pointer* (`dfs(i, current_total + nums[i])`), allowing the same number to be chosen repeatedly. The exclusion path handles shifting forward by popping the item and advancing the pointer index normally (`dfs(i + 1, current_total)`). Prune dead branches instantly via dual-tier guard constraints (`current_total > target` or `i >= len(nums)`).
* **Complexity:**
  * **Time:** Exponential (commonly approximated as $O(2^{t/m})$) where $t$ is the target value and $m$ is the minimum value inside the numbers array, representing the maximum possible depth allocation bounds of the selection tree.
    - *Note:* The exact complexity depends on the branching factor and pruning effectiveness. 
  * **Space:** $O(t/m)$ tracking the height configuration of the deep recursive call stack frames.
* **Pointer Flow:**
```text
Infinite reuse choice forks:
candidates = [2,3,6,7]
target = 7

                    dfs(i=0,total=0)
                      ([])
                     /             \
             Include 2          Exclude 2
            (stay i=0)          (i=1)
             /                     \
      dfs(0,2)                 dfs(1,0)
        [2]
       /   \
 +2(stay)   Skip 2
    |          |
 dfs(0,4)   dfs(1,2)
   [2,2]
   /     \
 +2       Skip
 |          |
dfs(0,6)  dfs(1,4)
 [2,2,2]
 /      \
+2       +3
 |        |
8>X    total=7 (Save [2,2,3])
```
* **Pattern Recognition:**
  * Use an index-anchored inclusion loop when:
    - The problem explicitly permits infinite or unrestricted reuse of the same array element across a single combination track.
    - The target condition forms a hard mathematical target ceiling that can be tracked via a rolling accumulation sum.
* **Core Insight:** Infinite reuse is achieved by halting pointer progression on the inclusion branch line. By forcing the recursive call to inherit the exact same index `i`, the algorithm stays parked on the current number, letting it stack onto the combination repeatedly until a boundary prune or success gate triggers. Advancing to `i + 1` is reserved strictly for the exclusion track, ensuring that once you decide to move past a number, it can never be accessed again, which naturally prevents duplicate permutations.
* **Mistakes Made:** The primary conceptual trap was miscalculating the base case exits on negative or missing boundaries. Forgetting to place the overflow constraint check `if current_total > target:` right at the absolute front of the recursive call stack causes the function to spiral out of bounds, trapping the engine inside an infinite recursion loop that ends in a system crash because it lacks a built-in cell limit to stop the continuous inclusion line.
* **What I Learned:** Freezing index pointer increments handles infinite element reuse elegantly. Coupling rolling accumulation parameters with fail-fast bounding guard lines protects the execution tree against out-of-bounds stack overflows. Unlike subsets, the inclusion branch does not advance the pointer because each number may be reused infinitely many times.

---

# Comparison

| Problem | Duplicate Handling | Element Reuse | Decision Style |
|----------|-------------------|---------------|----------------|
| Subsets | No duplicates | No reuse | Include / Exclude |
| Subsets II | Skip duplicates | No reuse | Include / Exclude + Pruning |
| Combination Sum | No duplicates | Infinite reuse | Include / Exclude (Frozen Index) |

---

# Recognition Signals

Think of Backtracking when you see words like:

* Generate all
* Find every
* Enumerate
* All combinations
* All subsets
* All permutations
* Partition
* Arrange
* Solve puzzle
* Explore every possibility
* Return all possible answers

Usually, if the answer requires **every valid configuration**, backtracking is a candidate.

---

### Master Patterns Learned

#### 1. The Binary Include-Exclude Paradigm (The State-Space Split Frame)
* **Applied to:** Subsets, Subsets II, Combination Sum
* **The Strategy:** Use this architectural template when a problem space can be modeled as a continuous series of binary choices (yes/no, pick/skip) across an ordered dataset. Instead of using horizontal loop ranges to advance trackers, drive a pure two-fork decision tree where the cursor index increments steadily, handling the full inclusion pipeline first before executing an immediate rollback to process the exclusion pipeline.
* **The Conceptual Mechanics:**
  - **Symmetric Choice Splitting:** Loop-based backtracking templates change window boundaries dynamically on every layer. The include-exclude model fixes state processing down to a clear, two-branch coordinate system. This layout isolates context shifts cleanly and forces snapshot saving actions to execute exclusively at the terminal leaf nodes (i ≥ n), guaranteeing all paths are fully evaluated.
  - **State-Tracking Purity:** Because each index element undergoes an identical binary lifecycle, the call stack memory remains completely balanced and protected against tracking out-of-bounds pointer crashes.
* **The Layout / Code Pattern:**
```python
def include_exclude_backtrack(dataset: list) -> list:
    global_results = []
    running_stack = []
    
    def dfs(index):
        # Base Case / Target Boundary Goal Check
        if index >= len(dataset):
            global_results.append(list(running_stack))          # Deep clone memory snapshot
            return
            
        # Branch Track 1: INCLUDE the active element node
        running_stack.append(dataset[index])
        dfs(index + 1)          # Explore deeper downstream paths
        
        # Branch Track 2: EXCLUDE the active element node (Rollback/Undo)
        running_stack.pop()
        dfs(index + 1)          # Explore alternative paths without the element
        
    dfs(0)
    return global_results
```
* **Examples:** Generating power sets, evaluating subsets with strict inclusion constraints, binary item combination algorithms, or zero-one subset picking operations.

#### 2. Post-Inversion Duplicate Throttling (The Exclusion Branch Pruner)
* **Applied to:** Subsets II
* **The Strategy:** Use this combination framework when an input array contains identical duplicated elements, but the structural constraints demand strictly unique combination sets. Group identical numbers together by sorting the array up front. Run the include-exclude model normally, but right after the inclusion track pops and rolls back, insert a lookahead condition loop that advances the pointer index past all matching duplicate values before launching the exclusion track.
* **The Conceptual Mechanics:**
  - **Pruning Contiguous Duplicate Domains:** Sorting elements turns matching duplicates into a single contiguous memory block. If you choose to skip a number, choosing to pick any subsequent copy of that same number further down the same track will produce a duplicate set.
  - **Exclusion-Gate Protection:** Running the lookahead loop (`while nums[i] == nums[i+1]`) exclusive to the *exclusion line* guarantees that the inclusion track can still legally collect multiple copies of the duplicate value to form subsets like `[2, 2]`, while protecting the alternative tracks from wastefully duplicating those exact same sets.
* **The Layout / Code Pattern:**
```python
def pruned_duplicate_backtrack(nums: list) -> list:
    results = []
    stack = []
    nums.sort()         # Step 1: Group matching duplicates contiguously
    
    def dfs(i):
        if i >= len(nums):
            results.append(list(stack))
            return
            
        # 1. Standard Inclusion Path
        stack.append(nums[i])
        dfs(i + 1)
        
        # 2. Rollback/Undo step
        stack.pop()
        
        # 3. Post-Inversion Throttling: Skip identical choices on the exclusion line
        while i + 1 < len(nums) and nums[i] == nums[i + 1]:
            i += 1          # Shift cursor past duplicate choices
            
        # 4. Standard Exclusion Path (Launches from newly pruned index boundary)
        dfs(i + 1)
        
    dfs(0)
    return results
```
* **Examples:** Finding subsets with duplicates, processing candidate item groups with identical weights, distinct letter permutation/combination trees, or multi-choice deduplicated item allocations.

#### 3. Index-Anchored Infinite Accumulation (The Unbounded Selector Frame)
* **Applied to:** Combination Sum
* **The Strategy:** Use this pattern when a combination optimization problem permits unrestricted, infinite reuse of individual elements across a single choice track. To simulate unbounded allocations within a structured binary choice tree, freeze pointer progression completely on the inclusion branch line, forcing the recursive step to inherit the exact same index `i`. Reserve index incrementing (`i + 1`) exclusively for the alternative exclusion path to guarantee that once you step past an element, it is permanently locked out.
* **The Conceptual Mechanics:**
  - **Index Immobilization:** Halting pointer updates on inclusion locks the algorithm onto the active number, letting it stack onto the configuration repeatedly. The track continues to ingest the same value until a fail-fast ceiling limit triggers.
  - **Permutation Lockout:** Advancing to `i + 1` exclusively on the exclusion line establishes an absolute boundary wall. Because the code never looks backward, once an item is bypassed, it is out of the selection pool completely, which naturally blocks duplicate permutations without extra hashing tables.
* **The Layout / Code Pattern:**
```python
def unbounded_target_search(candidates: list, target_ceiling: int) -> list:
    results = []
    combination_stack = []
    
    def dfs(i, running_sum):
        # Fail-Fast Bounding Constraints (Prune dead ends early)
        if running_sum == target_ceiling:
            results.append(list(combination_stack))
            return
        if i >= len(candidates) or running_sum > target_ceiling:
            return
            
        # Choice Track 1: INCLUDE element + FREEZE index pointer to permit infinite reuse
        combination_stack.append(candidates[i])
        dfs(i, running_sum + candidates[i])         # Index remains 'i'
        
        # Rollback/Undo
        combination_stack.pop()
        
        # Choice Track 2: EXCLUDE element + ADVANCE pointer to execute permanent lockout
        dfs(i + 1, running_sum)         # Index steps to 'i + 1'
        
    dfs(0, 0)
    return results
```
* **Examples:** Unbounded knapsack target combinations, infinite coin change selection combinations, numeric factorization paths, or repeated target value partition trees.