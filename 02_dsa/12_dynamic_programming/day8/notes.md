# Tree DP & Recursive State Passing

## 1. The Anatomy of Tree DP

In standard 1D or Grid DP, we dictate the traversal order through strict `for` loops (e.g., left-to-right, bottom-up). In **Tree DP**, the strict hierarchy of the data structure forces us to abandon loops entirely. The traversal order is intrinsically tied to Depth-First Search (DFS) recursive patterns.

Tree DP is mathematically identical to standard DP, but the dependencies are hierarchical: a parent node's optimal state is exclusively derived from the computed states of its left and right children.

---

## 2. Postorder Traversal: The Heartbeat of Tree DP

> **The Golden Rule of Tree DP:**
> If a parent requires information from its children to calculate its own optimal state, the DFS **must** execute in `Postorder` (Left $\rightarrow$ Right $\rightarrow$ Node).

In a Postorder DP, the recursive function dives all the way down to the leaf nodes. As the recursion unwinds, it bubbles the optimal states upward. The DP state transition equation executes exactly at the moment the parent regains control from both of its children.

---

## 3. The Dual-State Return (Include/Exclude on Trees)

In standard DP, we can store multiple states in a 2D array (e.g., `dp[i][0]` for skip, `dp[i][1]` for take). In Tree DP, we cannot rely on external arrays because node indexing is not strictly contiguous.

Instead, we bind the state directly into the recursive payload. The DFS function itself is engineered to return a **Tuple of states**.

```python
def dfs(node) -> tuple[int, int]:
    # Returns (optimal_if_node_included, optimal_if_node_excluded)
    left_included, left_excluded = dfs(node.left)
    right_included, right_excluded = dfs(node.right)
    
    # Execute Transitions
    node_included = node.val + left_excluded + right_excluded
    node_excluded = max(left_included, left_excluded) + max(right_included, right_excluded)
    
    return (node_included, node_excluded)
```

---

## Problem: House Robber III (337)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Postorder Dual-State DP
* **Problem Type:** Hierarchical Include/Exclude
* **Data Structure Used:** Implicit Call Stack (Tuple Return)
* **Brute Force:** Recursive DFS utilizing a `memo` dictionary keyed by node hashes. Time: $O(N)$ with heavy hashing overhead.
* **Optimized Approach:** We bypass the `memo` dictionary entirely by embedding the state into the return signature. Every node explicitly returns two values to its parent: the max money if this node IS robbed, and the max money if this node is SKIPPED.

### DP State
The recursive function returns `(rob_current, skip_current)`.
* `rob_current`: Max money subtree can generate if the current root is robbed.
* `skip_current`: Max money subtree can generate if the current root is completely ignored.

### State Flow
```text
STATE: Returning (robbed, skipped) up the tree.

↓

CHOICES at `node`:
  Condition A: We ROB this node.
    We are strictly forbidden from robbing its direct children.
    Money = node.val + left_child_skipped + right_child_skipped
    
  Condition B: We SKIP this node.
    The children are physically unlocked. We can independently choose 
    whatever was optimal for the left child (rob or skip) AND right child.
    Money = max(left_robbed, left_skipped) + max(right_robbed, right_skipped)

↓

TRANSITION: Return (Condition A, Condition B) to the parent.
```

### Recurrence
$$\text{rob} = \text{node.val} + \text{left.skip} + \text{right.skip}$$
$$\text{skip} = \max(\text{left.rob}, \text{left.skip}) + \max(\text{right.rob}, \text{right.skip})$$

### Base Cases
* If `node is None`, return `(0, 0)`. A non-existent node yields $0$ money regardless of choice.

### Traversal Order
**Strict Postorder.** (Left child resolves $\rightarrow$ Right child resolves $\rightarrow$ Current node calculates).

### Pointer Flow
```text
Tree:    3
        / \
       2   3
        \   \
         3   1

Leaf 3 (left subtree): rob=3, skip=0 -> returns (3,0)
Leaf 1 (right subtree): rob=1, skip=0 -> returns (1,0)

Node 2 (Left child of root):
  rob = 2 + 0 = 2
  skip = max(3,0) = 3
  returns (2,3)

Node 3 (Right child of root):
  rob = 3 + 0 = 3
  skip = max(1,0) = 1
  returns (3,1)

Root 3:
  rob = 3 + 3 (left skip) + 1 (right skip) = 7
  skip = max(2,3) + max(3,1) = 3 + 3 = 6
  returns (7,6)

Global Max = max(7, 6) = 7.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N) (Every node visited once)     │
│  Space Complexity │ O(H) (Height of the call stack)    │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Operating on a Binary Tree.
* ✓ Problem requires Include/Exclude logic with adjacency constraints.
* $\rightarrow$ **Postorder Dual-State DP**

### Core Insight
A parent node cannot dynamically query the grand-children of a binary tree easily. By forcing the children to calculate and return *both* possible temporal realities (robbed and skipped), the parent has all the $O(1)$ mathematical data it requires to make its own local decision.

### Mistakes Made
* We attempted to calculate `skip_current = left_robbed + right_robbed`. This is a critical logical flaw. Just because we skip the parent does NOT mandate that we *must* rob the children. We merely *unlock* the children. The correct logic is to take the `max(rob, skip)` for each child independently.

### What I Learned
The DP state in trees is fluidly passed through the return payload of the recursive signature. This completely eliminates the need for massive `dp` arrays or complex hashing dictionaries.

---

## Problem: Binary Tree Maximum Path Sum (124)

* **Interview Difficulty:** Hard
* **Parent Pattern:** Path Extraction DP
* **Problem Type:** Nonlinear Global Maximization
* **Data Structure Used:** Implicit Call Stack + Global Tracking Variable.
* **Brute Force:** From every single node, run a DFS to find the max path. Time: $O(N^2)$.
* **Optimized Approach:** A valid path can only fork *once* (forming an arch). We use a global tracking variable `self.global_max`. At every node, we calculate the max arch `(left + node + right)` and aggressively attempt to update the global max. However, a node CANNOT return a forked arch back to its parent, as that would create a mathematically invalid 3-way intersection. It strictly returns the single best linear path `(node + max(left, right))`.

### DP State
The recursive function returns the **maximum linear path sum descending downward from the current node**. 

### State Flow
```text
STATE: return max linear path. Maintain global_max arch.

↓

CHOICES at `node`:
  Step 1: Sanitize Children.
    If a child returns a negative path sum, it will actively drag our score down.
    We simply refuse to walk down that path. max(child_sum, 0).
  
  Step 2: Update Global Architecture.
    Calculate the local Arch passing through this node: left + right + node.val
    self.global_max = max(self.global_max, Arch)
    
  Step 3: Return Linear Continuity.
    We must provide our parent with a single, straight line.
    Return: node.val + max(left, right)

↓

TRANSITION: Return linear path, but quietly update global_max.
```

### Recurrence
$$\text{Linear Return} = \text{node.val} + \max(\text{left\_linear}, \text{right\_linear})$$
$$\text{Global Arch} = \text{node.val} + \text{left\_linear} + \text{right\_linear}$$

### Base Cases
* If `node is None`, return `0` (an empty path contributes 0 to the sum).
* `self.global_max` initialized to `float('-inf')` to support purely negative trees.

### Traversal Order
**Strict Postorder.**

### Pointer Flow
```text
Tree:   -10
        /  \
       9   20
          /  \
         15   7

Leaf 9: returns 9. global_max = 9.
Leaf 15: returns 15. global_max = 15.
Leaf 7: returns 7. global_max = max(15, 7) = 15.

Node 20:
  Arch = 15 + 7 + 20 = 42. global_max = max(15, 42) = 42.
  Returns linear path to parent: 20 + max(15, 7) = 35.

Root -10:
  Arch = 9 + 35 + (-10) = 34. global_max remains 42.
  Returns: -10 + max(9, 35) = 25.

Final Output is the global tracker: 42.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N)                               │
│  Space Complexity │ O(H) (Height of the call stack)    │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Operating on a Binary Tree.
* ✓ Prompt allows paths to traverse "up and over" a node.
* $\rightarrow$ **Path Extraction DP (Arch vs Linear)**

### Core Insight
A tree path can only change its vertical direction (going up, then going down) exactly **once**. We bifurcate the logic: the global tracker handles the one-time arch, while the recursive return payload strictly enforces the linear, non-forking geometry required by the parent.

### Mistakes Made
* We forgot to sanitize negative child returns. If a left subtree yields `-5`, including it mathematically damages the path. By explicitly wrapping the child returns in `max(dfs(node.left), 0)`, we elegantly execute a localized "skip" maneuver, pruning toxic branches natively.

### What I Learned
Global trackers combined with restricted linear return signatures form the absolute standard blueprint for all complex Tree pathfinding algorithms.

---

## Problem: Diameter of Binary Tree (543)

* **Interview Difficulty:** Easy
* **Parent Pattern:** Path Extraction DP (Unweighted)
* **Problem Type:** Depth Maximization
* **Data Structure Used:** Implicit Call Stack + Global Tracking Variable.
* **Brute Force:** DFS from every node. Time: $O(N^2)$.
* **Optimized Approach:** This is a structurally stripped-down clone of *Binary Tree Maximum Path Sum*. Instead of calculating heavy integer weights, we merely count physical edges. The diameter passing through a node is simply `left_depth + right_depth`. The node returns its own depth `(1 + max(left, right))` to its parent.

### DP State
The recursive function returns the **maximum edge depth descending from the current node**.

### State Flow
```text
STATE: return max depth. Maintain global max diameter.

↓

CHOICES at `node`:
  Step 1: Calculate local diameter (Arch passing through this node).
    Diameter = left_depth + right_depth
    self.max_diameter = max(self.max_diameter, Diameter)
    
  Step 2: Return linear depth to parent.
    Return: 1 + max(left_depth, right_depth)

↓

TRANSITION: Return 1 + max(L, R).
```

### Recurrence
$$\text{Return Value} = 1 + \max(\text{left}, \text{right})$$

### Base Cases
* If `node is None`, return `0` (depth of a non-existent node is 0).

### Traversal Order
**Strict Postorder.**

### Pointer Flow
*(Identical architecture to Max Path Sum, but utilizing scalar `+1` incrementation instead of `node.val` weights).*

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N)                               │
│  Space Complexity │ O(H)                               │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Binary Tree metric requiring the "longest" physical path between any two nodes.
* $\rightarrow$ **Path Extraction DP (Arch vs Linear)**

### Core Insight
The longest path in any tree MUST arc over some specific node (even if that node is the root itself). By calculating the `left + right` span at every single node and globally tracking the maximum, we mathematically guarantee discovering the widest span in $O(N)$ time.

### Mistakes Made
* We attempted to return the diameter directly up the recursive chain. This crashes the logic because a diameter represents a completed path (an arch), and a parent node cannot append itself to a path that has already forked in two directions.

### What I Learned
Return exactly what the parent requires to build its own state (a single straight line), and use an external mechanism (global variable) to track the final answer.

---

## Problem: Longest ZigZag Path in a Binary Tree (1372)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Preorder State Passing DP
* **Problem Type:** Top-Down Path Validation
* **Data Structure Used:** Implicit Call Stack with Top-Down Argument Passing.
* **Brute Force:** N/A.
* **Optimized Approach:** Unlike the previous three problems that bubbled answers upward via Postorder, ZigZag tracking relies on **Preorder traversal**. The parent must tell the child: *"I just moved Left to reach you. You MUST move Right to keep the combo alive. Your current streak is 3."* The child receives this state, attempts the valid move to extend the streak, and attempts the invalid move which immediately resets the streak back to 1.

### DP State
The recursive payload explicitly passes the state **DOWNWARD**: `dfs(node, is_left_direction, current_length)`.

### State Flow
```text
STATE: Receive (is_left, length). Update global max. Pass new states downward.

↓

CHOICES at `node`:
  If we arrived via a LEFT step (is_left == True):
    - Moving RIGHT continues the combo: dfs(node.right, False, length + 1)
    - Moving LEFT shatters the combo: dfs(node.left, True, 1)
    
  If we arrived via a RIGHT step (is_left == False):
    - Moving LEFT continues the combo: dfs(node.left, True, length + 1)
    - Moving RIGHT shatters the combo: dfs(node.right, False, 1)

↓

TRANSITION: Pass incremented length to the opposite child. Pass reset length (1) to the identical child.
```

### Recurrence
(Implemented directly within the DFS parameter payload rather than an algebraic return equation).

### Base Cases
* If `node is None`, terminate branch execution (`return`).
* The Root initiates two independent path injections: `dfs(root.left, True, 1)` and `dfs(root.right, False, 1)`.

### Traversal Order
**Strict Preorder.** (State arrives from parent $\rightarrow$ Node processes $\rightarrow$ Node passes state down to children).

### Pointer Flow
```text
Tree: Right-heavy ZigZag path.

Root triggers: dfs(root.right, False, 1)

Node (Right of Root):
  Receives: (is_left=False, length=1). Updates max to 1.
  Triggers opposite child: dfs(node.left, True, 2)
  Triggers same child (Reset): dfs(node.right, False, 1)

Node (Left child of the Right node):
  Receives: (is_left=True, length=2). Updates max to 2.
  Triggers opposite child: dfs(node.right, False, 3)
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N)                               │
│  Space Complexity │ O(H)                               │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Operating on a Binary Tree.
* ✓ The validity of a node's move is entirely dictated by the historical action taken by its parent.
* $\rightarrow$ **Preorder State Passing DP**

### Core Insight
When a tree problem demands a sequence validation based on historical parent actions, Postorder bubbling fails because children don't know how they were reached. We must invert the DP flow, injecting the state variables directly into the parameters of the DFS function to push them top-down.

### Mistakes Made
* We attempted to execute this using Postorder bubbling, having the children return their max left and right zigzags. While possible, the transition logic became incredibly convoluted. Recognizing that the state dependency flows Top-Down immediately simplified the architecture.

### What I Learned
The direction of state dependency dictates the traversal order. 
* Child state depends on Parent $\rightarrow$ Preorder (State passed in parameters).
* Parent state depends on Child $\rightarrow$ Postorder (State passed in returns).

---

### Master Patterns Learned

#### 1. The Postorder Dual-State Return (Include/Exclude)
* **The Strategy:** Deploy whenever a parent node must make a binary choice (Rob/Skip, Color Red/Color Blue) that is structurally restricted by the choices its children made.
* **The Conceptual Mechanics:** Because we cannot use 2D DP arrays for trees, we embed the dual states directly into a tuple return payload `(state_A, state_B)`. The parent unwraps the tuples from its left and right children and executes the maximization equation locally.

#### 2. The Path Arching Global Tracker
* **The Strategy:** Deploy whenever finding the "Maximum Path", "Longest Path", or "Diameter" of a tree.
* **The Conceptual Mechanics:** A valid path can only arch over a node once. The recursive return signature MUST be restricted to a single linear line to prevent invalid multi-forking. The actual arch calculation is offloaded entirely to a `global_max` tracking variable that quietly updates itself as the recursion unwinds.

#### 3. Top-Down Parameter Injection
* **The Strategy:** Deploy whenever the validity of a child's action is governed by the historical sequence of its ancestors.
* **The Conceptual Mechanics:** Invert standard Tree DP. Do not return values. Instead, pass the accumulated DP state (length, direction, accumulated sum) downward as explicit parameters in the DFS signature.
