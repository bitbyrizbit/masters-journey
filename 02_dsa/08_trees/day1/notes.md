# Trees

## Core Syntax
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```


## DFS Traversals

### Preorder
Node → Left → Right

```python
def dfs(node):
    if not node:
        return
    print(node.val)
    dfs(node.left)
    dfs(node.right)
```

### Inorder
Left → Node → Right

```python
def dfs(node):
    if not node:
        return
    dfs(node.left)
    print(node.val)
    dfs(node.right)
```

### Postorder
Left → Right → Node

```python
def dfs(node):
    if not node:
        return
    dfs(node.left)
    dfs(node.right)
    print(node.val)
```


## Golden Rules
1. Every subtree is itself a tree.
2. Always identify recursion base case first.
3. Ask:
   - Am I modifying tree?
   - Returning subtree info?
   - Combining left + right answers?
4. Preorder → mutate/process node first.
5. Inorder → mostly BST problems.
6. Postorder → height / diameter / balance.
7. For tree recursion, always ask:
   - What should this function RETURN?
   - Or is it just mutating the tree?

*Note:* Trees become much easier once you classify problems into mutation problems like invert tree or flatten tree, return-value problems like max depth, balanced tree or diameter, or traversal-only problems like BFS level order, preorder print.


## Common Bugs
- Forgetting `if not node`
- Returning wrong recursive value
- Mixing traversal logic
- Accessing `.left` on `None`

---

## Problem: Invert Binary Tree

* **Problem Type:** Tree Mutation / Recursive DFS (Preorder Traversal)
* **Data Structure Used:** Binary Tree
* **Approach 1:** Iterative Level-Order Traversal (BFS). Push the root into a `deque` and process level by level. At every node popped, perform a structural swap of its left and right pointers using a temporary reference variable, then append the existing child nodes back into the queue. This avoids call stack memory overhead but incurs an $O(n)$ queue spatial footprint.
* **Optimized Approach:** Top-Down Recursive Depth-First Search (DFS). Swap the direct left and right memory addresses of the parent node immediately upon entrance, and then recursively invoke the function down both branches to propagate the mirror inversion down to the leaves.
* **Complexity:**
  * **Time:** $O(n)$ because the algorithm must land on every individual node exactly once to perform the swap.
  * **Space:** $O(h)$ where $h$ is the maximum tree height, consumed entirely by the recursive function call frames. In the worst case of a skewed linear tree, this degrades to $O(n)$; for a perfectly balanced tree, it minimizes to $O(\log n)$.
* **Pointer Flow:**
```text
Before:
      4
     / \
    2   7
   / \ / \
  1  3 6  9

Execution step at Root (Node 4):
root.left, root.right = root.right, root.left  # Swaps entire structural layouts

Intermediate State:
      4
     / \
    7   2
   / \ / \
  6  9 1  3

Cascading Downward Recurrences:
invertTree(7) -> Inverts leaves 6 and 9 into 9 and 6
invertTree(2) -> Inverts leaves 1 and 3 into 3 and 1

Final Structure:
      4
     / \
    7   2
   / \ / \
  9  6 3  1
```
* **Pattern Recognition:**
  * Use a top-down preorder mutation strategy when:
    - The processing or rearrangement of a node can be executed safely before exploring its children.
    - Swapping higher-level pointer paths naturally alters the traversal coordinates for all downstream recursive operations.
* **Core Insight:** Because a binary tree is structurally recursive, a parent node acts as a gateway anchor. Swapping `root.left` and `root.right` moves the *entire* downstream subtree memory structure simultaneously. This means a top-down preorder swap automatically redirects the paths for subsequent recursive calls, allowing the inversion to propagate perfectly without losing any subtree references.
* **Mistakes Made:** Trying to perform sequential assignment steps without Python's simultaneous unpacking syntax (`root.left, root.right = root.right, root.left`). Writing them as individual lines without an external temporary holding variable causes one of the subtree memory addresses to overwrite the other, completely severing an entire branch of data from memory.
* **What I Learned:** Structural mutations are cleanest when handled from the top down. Processing the current root before its children allows the recursive mechanism to smoothly step directly into the newly rearranged pointer positions on subsequent frames.

---

## Problem: Maximum Depth of Binary Tree

* **Problem Type:** Bottom-Up Functional Accumulation / Recursive Postorder
* **Data Structure Used:** Binary Tree
* **Approach 1:** Iterative BFS Traversal. Deploy a queue to process the tree layer by layer, tracking depth by running an inner loop that completely drains all elements belonging to the current level before incrementing a scalar depth counter. This protects against stack overflow limitations but demands $O(n)$ storage memory for wide levels.
* **Optimized Approach:** Bottom-Up Recursive DFS. Query the depths of the left and right subtrees independently, isolate the larger value using a maximum extraction check, and bubble the result up to the parent layer by adding a $+1$ offset to account for the current node's level.
* **Complexity:**
  * **Time:** $O(n)$ because computing a global structural limit requires analyzing every node in the graph.
  * **Space:** $O(h)$ where $h$ is the tree height, measuring the maximum call stack memory allocated during deep execution paths.
* **Pointer Flow:**
```text
Evaluating tree levels from the leaves up to the root:
       3
      / \
     9  20
       /  \
      15   7

maxDepth(9)  -> Left: 0, Right: 0 -> returns max(0, 0) + 1 = 1
maxDepth(15) -> Left: 0, Right: 0 -> returns max(0, 0) + 1 = 1
maxDepth(7)  -> Left: 0, Right: 0 -> returns max(0, 0) + 1 = 1

maxDepth(20) -> Left child (15) returns 1
                Right child (7) returns 1
                returns max(1, 1) + 1 = 2

maxDepth(3)  -> Left child (9) returns 1
                Right child (20) returns 2
                Final result: max(1, 2) + 1 = 3
```
* **Pattern Recognition:**
  * Use a bottom-up postorder accumulation strategy when:
    - The score or evaluation metric of a parent node depends entirely on data values computed by its children.
    - Base layers (leaves) must declare their boundaries first before upper layers can resolve geometric sums.
* **Core Insight:** Evaluating tree height requires a postorder mindset. A parent node is structurally incapable of determining its maximum depth boundary until both its left and right subtrees have completely finished calculating their independent internal paths and returned their scalar maximums.
* **Mistakes Made:** The primary conceptual block was managing the terminal null boundaries correctly. Forgetting that a missing leaf's virtual child must evaluate to a depth baseline of `0` (`if not root: return 0`) causes the calculation layer to crash when it attempts to run comparison arithmetic on empty or non-existent pointer objects.
* **What I Learned:** Postorder traversals are the ultimate tool for tree aggregation questions. Allowing subproblems to execute independently and bubble their values back up enables the parent node to solve complex geometric limits using simple, constant-time math.

---

## Problem: Diameter of Binary Tree

* **Problem Type:** Dual-State Global Tracking / Bottom-Up Postorder Accumulation
* **Data Structure Used:** Binary Tree
* **Approach 1:** For every node, calculate: left subtree height + right subtree height, and track maximum over all nodes. Since each height calculation costs $O(n)$ repeating for every node leads to $O(n²)$.
* **Optimized Approach:** Execute a bottom-up postorder traversal that computes the vertical height of each subtree. While returning this height to the parent node, simultaneously add the left and right subtree heights together (`left + right`) at the current node to evaluate and update a persistent global state tracker `self.diameter` on the fly.
* **Complexity:**
  * **Time:** $O(n)$ since each node is visited exactly once to calculate heights and check diameters.
  * **Space:** $O(h)$ auxiliary memory space corresponding directly to the maximum height call stack depth.
* **Pointer Flow:**
```text
Updating the global diameter state dynamically during height calculation:
        1
       / \
      2   3
     / \
    4   5

maxDepth(4) -> Height: 1, Global diameter updated: max(0, 0+0) = 0
maxDepth(5) -> Height: 1, Global diameter updated: max(0, 0+0) = 0

maxDepth(2) -> Receives Left child height = 1, Right child height = 1
               Local path span: left + right = 1 + 1 = 2
               Global diameter updated: max(0, 2) = 2
               Returns height to parent: max(1, 1) + 1 = 2

maxDepth(3) -> Height: 1, Global diameter updated: max(2, 0+0) = 2

maxDepth(1) -> Receives Left height from node 2 = 2, Right height from node 3 = 1
               Local path span: left + right = 2 + 1 = 3
               Global diameter updated: max(2, 3) = 3
               Returns height to parent: max(2, 1) + 1 = 3
```
* **Pattern Recognition:**
  * Use a global state-tracking postorder strategy when:
    - The optimal target sub-path is non-linear and may exist completely within a deeply nested sub-root, instead of passing through the top-level head.
    - You must decouple the value returned up the recursive call stack from the global maximum metric you are actively hunting for.
* **Core Insight:** The diameter of a tree does not necessarily have to cross through the root node—it can be entirely contained inside a long, lopsided subtree. By tracking the global maximum via a class attribute (`self.diameter`), you can measure the combined left-and-right split path at every single node, while safely continuing to return a simple single vertical height line up to the calling frame.
* **Mistakes Made:** The hardest thought-driven hurdle was resisting the urge to return the diameter calculation directly up the recursive call stack. Attempting to return the diameter breaks the recursive logic completely, because a parent node can only build its own height using a single, continuous vertical path line from its children. A split path (`left + right`) cannot be extended upward.
* **What I Learned:** Dual-tracking structures provide massive performance optimizations. Updating a persistent global tracker during a linear postorder execution pass allows you to evaluate every split path intersection combination in a single sweep, keeping execution times down to a clean linear scale.

---

### Master Patterns Learned

#### 1. Preorder = Parent-First Mutation
* **Applied to:** Invert Binary Tree
* **The Strategy:** Use a top-down preorder approach when an operation or structural mutation executed at a parent node naturally configures or fixes the path vectors for all downstream children. Processing the root node first eliminates the need to maintain historical tracking states or complex coordinate maps as the recursion dives deeper.
* **The Layout / Code Pattern:**
```python
def mutate_tree(node):
    if not node:
        return None     # Base Case
        
    # Execute structural mutation on parent FIRST
    node.left, node.right = node.right, node.left 
    
    # Cascade mutation down to downstream subtrees
    mutate_tree(node.left)
    mutate_tree(node.right)
    return node
```
* **Examples:** Inverting a binary tree, serializing/deserializing tree structures, flattening a binary tree into a linked list, or copying/cloning node allocations.

#### 2. Postorder = Bottom-Up Accumulation
* **Applied to:** Maximum Depth of Binary Tree
* **The Strategy:** Use a bottom-up postorder strategy when a parent node is structurally incapable of determining its own score or state until its children have fully resolved their internal subproblems and returned their independent results up the execution stack.
* **The Layout / Code Pattern:**
```python
def evaluate_tree(node):
        return 0    # Base Case: Terminal leaves carry zero metric weight
    if not node:
        
    # Recurse fully to collect answers from children FIRST
    left_metric = evaluate_tree(node.left)
    right_metric = evaluate_tree(node.right)
    
    # Bubble up calculation to the parent using child boundaries
    return max(left_metric, right_metric) + 1
```
* **Examples:** Calculating tree height/depth, verifying if a binary tree is height-balanced, or finding the lowest common ancestor (LCA).

#### 3. Global State Tracking DFS (The Dual-Information Pattern)
* **Applied to:** Diameter of Binary Tree
* **The Strategy:** Use this architecture when a recursive function needs to compute two pieces of information at once: a local value that must return up the call stack to keep the parent's math valid, and a global extreme metric that can exist anywhere across the structural graph. By decoupling the return value from the target solution, a primitive tracker captures the optimal answer across deep splits in a single pass.
* **The Layout / Code Pattern:**
```python
class Solution:
    def targetProblem(self, root: TreeNode) -> int:
        self.global_maximum = 0     # Global state tracker
        
        def bottom_up_dfs(node):
            if not node:
                return 0    # 1. Base Case
                
            # 2. Recurse down to isolate child values
            left_info = bottom_up_dfs(node.left)
            right_info = bottom_up_dfs(node.right)
            
            # 3. Structural Evaluation: Update global tracking metric
            # Combines both split paths dynamically at the local root
            self.global_maximum = max(self.global_maximum, left_info + right_info)
            
            # 4. Return Value: Send only a singular valid branch line upward
            return max(left_info, right_info) + 1
            
        bottom_up_dfs(root)
        return self.global_maximum
```
* **Examples:** Evaluating tree diameter, finding the maximum path sum across arbitrary paths, calculating the longest univalue path, or isolating the largest binary search subtree (BST) hidden inside a general binary tree structure.