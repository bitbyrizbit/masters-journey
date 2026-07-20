# Topological Sort (DAGs)

## 1. Directed Acyclic Graph (DAG)

### What is a Directed Graph?
A **Directed Graph (Digraph)** is a network of nodes where every connection or edge possesses a strict one-way direction vector ($\rightarrow$). Moving across an edge from node $u$ to node $v$ is a legal operation, but moving backward from $v$ to $u$ is completely illegal unless an independent, explicit reverse edge ($v \rightarrow u$) is configured in the graph layout.

### What is a DAG?
A **Directed Acyclic Graph (DAG)** is a directed graph that contains **absolute zero cyclic loops**. If you start a traversal path at any arbitrary vertex inside a DAG and continuously follow the unidirectional edge arrows forward, it is physically and mathematically impossible to ever loop back around to touch any previously visited vertex.

### Why Cycles Make Ordering Impossible
A dependency cycle represents a state of structural gridlock. If Task A requires Task B to finish first, Task B requires Task C, and Task C requires Task A, you enter a circular logic loop:

```text
    (Task A) -------> (Task B)
       ^                 |
       |                 v
       +-------------- (Task C)   <-- Structural Gridlock!
```
To start Task A, you must complete Task C; to complete Task C, you must finish Task B; to finish Task B, you must complete Task A. Because no task can act as an absolute starting anchor point, a valid chronological layout order cannot exist.

### Real-World Intuition
*   **Course Prerequisites:** Academic curriculums where advanced research courses require completing foundational introductory tracks first.
*   **Build Systems:** Compiling complex software architectures (like C++ or monorepos) where target libraries require compiling prerequisite data modules ahead of time.
*   **Task Scheduling:** Managing a workflow or pipeline (e.g., automated factory assembly lines) where specific operations must execute in a precise linear sequence.
*   **Package Dependencies:** Software package installers (like `npm` or `pip`) downloading and configuring low-level foundational libraries completely before building out upper application tools.

---

## 2. What is Topological Ordering?

### Definition
A **Topological Sort** of a Directed Acyclic Graph (DAG) is a linear ordering of all its vertices such that for every directed one-way edge $u \rightarrow v$, vertex $u$ appears strictly *before* vertex $v$ inside the sequence array. 

### Multiple Valid Orderings
Topological sort is **not unique**. A single graph layout can possess multiple distinct, valid linear orderings depending on which independent parallel streams your traversal chooses to explore first.

```text
Graph Layout:  (0) ----> (1) ----> (3)
                \                  ^
                 v                /
                (2) -------------+
```
*   **Valid Order 1:** `0 -> 1 -> 2 -> 3` (Processes top branch first)
*   **Valid Order 2:** `0 -> 2 -> 1 -> 3` (Processes bottom branch first)

### When One Does Not Exist
If a graph contains even a single hidden directional cycle or cross-link loop, **a topological ordering does not exist**. The structural gridlock breaks the linear constraints completely.

### Mathematical Properties
*   **Source Nodes:** Every valid DAG is guaranteed to possess at least one source vertex node (indegree = $0$) that can act as an absolute, dependency-free starting line.
*   **Sink Nodes:** Every valid DAG contains at least one sink vertex node (outdegree = $0$) representing a terminal task that depends on others but frees up no downstream paths.

---

## 3. Kahn's Algorithm (BFS Topological Sort)

### Indegree Concept
The **Indegree** of a vertex is the absolute scalar count of directed incoming edges pointing straight into that node. It measures exactly how many unresolved prerequisite dependencies a task must wait for before it can be legally executed.

### Computing Indegrees
Before launching Kahn's loop, run a full initialization pass across the adjacency tree: for every node $u$, iterate through its neighbor list, and increment `indegree[neighbor] += 1`.

### Queue Initialization
Scan your compiled indegree register map. Identify **every single node where indegree == 0**, and inject them concurrently into a FIFO data queue buffer. These nodes have zero prerequisite locks, acting as our initial dependency-free starting anchors.

### Processing Nodes & Decreasing Neighbors' Indegrees
Pop the front node from the queue and append it to your final sorted result list. Because this task is now completed, its out-going edges are wiped out. Loop through all its downstream neighbors, and decrement their dependency counts by exactly $-1$ (`indegree[neighbor] -= 1`). The absolute moment a neighbor's indegree drops down to exactly `0`, its final dependency lock has broken—append it to the queue immediately to join the active selection pool.

### Detecting Cycles
If the final length of your sorted answer array is smaller than the total vertex count of the graph (`len(answer) != V`), **the graph contains a cycle**. Kahn's algorithm handles cycle detection automatically because nodes trapped inside a circular dependency ring can never have their indegrees drop to 0, leaving them permanently locked out of the queue.

### Code Archetype Template
```python
from collections import deque

def kahns_topological_sort(V: int, adj_list: dict) -> list[int]:
    # 1. Initialize and compute indegrees across all vertices
    indegree = {i: 0 for i in range(V)}
    for node in adj_list:
        for neighbor in adj_list[node]:
            indegree[neighbor] += 1
            
    # 2. Queue all dependency-free baseline source nodes (Indegree == 0)
    queue = deque([i for i in range(V) if indegree[i] == 0])
    topological_order = []
    
    # 3. Interleaved Processing Loop
    while queue:
        node = queue.popleft()
        topological_order.append(node)
        
        for neighbor in adj_list[node]:
            indegree[neighbor] -= 1             # Erase dependency link
            if indegree[neighbor] == 0:
                queue.append(neighbor)          # Lock broken: push to active pool
                
    # 4. Cycle Check Verification Gate
    if len(topological_order) != V:
        return []           # Cycle detected! Ordering is mathematically impossible.
        
    return topological_order
```

---

## 4. DFS Topological Sort

### Postorder DFS Mechanics
DFS topological sorting runs in reverse using a bottom-up **Postorder Traversal** (`Children -> Parent`). Instead of building the path from the front, you dive down to the absolute bottom of the graph first to locate a terminal sink node ($0$ outdegree).

### Push After Exploring
Inside the recursive framework, you loop through and fully explore *all available downstream child branches completely first*. Only when a vertex has finished processing its entire neighborhood domain and is ready to pop off the execution call stack frame do you append its ID token onto a global results collector list (`answer.append(node)`).

### Reverse Answer Strategy
Because terminal sink nodes finish processing first, they settle at the absolute front of your raw collector list. To transform this bottom-up collection into a correct, top-down chronological dependency sequence, you **must execute a full array reversal** (`answer.reverse()`) right before exiting the module.

### Why This Works
If a directed edge exists from $u \rightarrow v$, then $v$ is a downstream child dependency of $u$. In a deep postorder DFS run, the recursive call frame for $v$ is guaranteed to completely finish and exit *before* the frame for $u$ can close. Therefore, $v$ will always land inside the collector list ahead of $u$. Reversing the final array flips this relationship perfectly, placing the prerequisite parent $u$ strictly ahead of its child dependency $v$.

### Code Archetype Template
```python
def dfs_topological_sort(V, adj_list):
    visited = set()
    postorder_collector = []
    
    def dfs(node):
        visited.add(node)
        
        # Explore all downstream child dependencies completely first
        for neighbor in adj_list[node]:
            if neighbor not in visited:
                dfs(neighbor)
                
        # Postorder Injection: Push to collector only when call frame closes
        postorder_collector.append(node)

    # Master loop handles disconnected components safely
    for vertex_id in range(V):
        if vertex_id not in visited:
            dfs(vertex_id)
            
    # Reverse the bottom-up collection to output chronological top-down sequence
    postorder_collector.reverse()
    return postorder_collector
```

---

## 5. Cycle Detection Frameworks

To prevent system crashes, you must isolate and handle structural cycles based strictly on the graph's structural edge categories.

### Undirected Graphs: Parent Tracking
Undirected edges are bidirectional roads. If you travel from node $A$ to node $B$, looking backward from $B$ will naturally show $A$ as an immediate neighbor. To prevent false-positive cycle triggers, you must pass a **`parent` tracking variable** down the call stack. If a neighbor node is already visited, it represents a true loop cycle *only if* that neighbor is not the direct parent node you just stepped from.

### Directed Graphs: Recursion Stack & Three-State Coloring
In a directed graph, parent tracking is completely broken because edges are one-way tracks. Cycle detection requires tracking whether a path intersects a node that is currently active inside the *current call stack branch path*.

1.  **The Recursion Stack Method:** Maintain a secondary boolean mask array or hash set `rec_stack`. Add a node to `rec_stack` upon entry, and remove it upon exit. If a neighbor is already visited and currently exists inside `rec_stack`, you have caught a back-edge loop, proving a cycle exists.
2.  **Three-State Coloring (The Academic Standard):** Map all vertices to three distinct conceptual memory color codes:
    *   `WHITE (0)`: Completely unvisited and undiscovered.
    *   `GRAY (1)`: Active. Node is loaded onto the call stack; its downstream subtrees are actively being explored.
    *   `BLACK (2)`: Solved. Node and all its downstream child branches are completely finished and popped off the stack.
    *   *Cycle Trigger:* If a traversal steps from a `GRAY` node and hits a neighbor that is also currently marked `GRAY`, a cycle is confirmed.

### Why Kahn's Algorithm Also Detects Cycles
Kahn's algorithm handles cycle detection implicitly through simple counting physics. A vertex can only enter the FIFO queue if its incoming indegree counter drops to exactly `0`. If a group of nodes forms a closed circular ring, every node in that ring has at least one prerequisite edge locked inside the circle. Because no outside wave can break into the ring to clear those internal dependencies, their indegree counts can never reach 0. They stay trapped in memory, causing the final processed node count to fall short of the total vertex total.

---

## 6. Comparing DFS vs. Kahn (BFS Topological Sort)

| Evaluation Vector | DFS Topological Sort | Kahn's Algorithm (BFS) |
| :--- | :--- | :--- |
| **Execution Engine** | Implicit Call Stack Recursion | Explicit FIFO Data Queue Buffer |
| **Core Traversal Style** | Bottom-Up Postorder Processing | Top-Down Dependency Draining |
| **Master Tracking Metric** | Call Frame Closure Order | Rolling Indegree Dependency Counts |
| **Memory Allocation** | Recursive Stack Allocation Frames | Flat Iterative Integer Map Buffers |
| **Cycle Detection Path** | Explicit Visited Stack / Gray Color Checks | Implicit Node Count Verification Gates |
| **Topology Behavior** | Deeply explores a single lineage track | Processes all available parallel tracks concurrently |

---

## 7. Common Patterns

*   **Course Scheduling:** Standard course prerequisite lock resolution (e.g., Course Schedule I & II).
*   **Dependency Resolution:** Packaging scripts determining compilation orders for interconnected software components.
*   **Build Order:** Build frameworks (like Make or Bazel) configuring build orders across complex module trees.
*   **Task Scheduling:** Resource allocators scheduling dependent events to minimize idle gaps.
*   **Alien Dictionary:** Deriving an un-ordered alphabet sequence by sorting characters based on sorted string dictionary lexicographical matches.
*   **Detect Cycles in DAG:** Verifying graph validation rules before launching deep pipelines.
*   **Longest Path in DAG:** Standard Dynamic Programming over topological sorting lines to extract longest traversal counts.

---

## 8. Common Mistakes

### Forgetting to Compute Indegrees Correctly
Miscounting initial edge connections by incrementing the source node instead of the destination node (`indegree[u]` instead of `indegree[v]`). This reverses your dependency arrows completely, causing Kahn's algorithm to output an inverted order.

### Not Initializing Queue with Every Indegree-0 Node
Only pushing the absolute first vertex index into the queue at startup. If a graph contains multiple independent parallel entry points or disconnected components, omitting them freezes execution early, leaving half your network completely unprocessed.

### Forgetting to Decrement Indegree
Popping a node and iterating through neighbors without writing the decrement step `indegree[neighbor] -= 1`. This leaves neighbor dependency counts permanently frozen above 0, preventing tasks from ever entering the active queue pipeline.

### Forgetting the Processed-Node Count Check
Returning a partially compiled topological array blindly without verifying its final length against the graph's vertex total. If a hidden cycle exists, the code will silently output a truncated, incomplete sequence, resulting in silent bugs down the line.

### Reversing DFS Result Incorrectly
Forgetting to call `.reverse()` on your postorder DFS collector list before returning it. This outputs a backwards dependency sequence, forcing terminal sink nodes to execute before their prerequisites.

### Using Topological Sort on Undirected Graphs
Attempting to run a topological ordering loop over an undirected graph network. Because undirected edges are inherently bidirectional, every single edge pair acts as a mutual cycle loop ($u \rightarrow v$ and $v \rightarrow u$), which breaks Kahn's algorithm instantly and leaves your queues empty.

---

## Problem: Course Schedule

* **Problem Type:** Cycle Detection in Directed Graphs / Topological Feasibility Check
* **Data Structure Used:** Adjacency List Map (`dict`) + Indegree Tracker Array (`list[int]`) + FIFO Queue (`collections.deque`)
* **Approach 1:** N/A
* **Optimized Approach:** Kahn's BFS Algorithm for Dependency Draining. Flatten raw dependency pairs into a unidirectional adjacency list mapping prerequisite source nodes to dependent target nodes. Concurrently, compute an `indegree` array where each index tracks how many prerequisite blockers that specific course must wait for. Initialize a `deque` pre-loaded with every single course code that holds an `indegree == 0`. While the queue drains via constant-time `.popleft()` extractions, increment a global `visited_count` counter, iterate through its neighbors, and decrement their dependency links by exactly -1. The absolute split-second any neighbor's indegree drops down to exactly `0`, its locks are broken—append it to the queue immediately. Return `True` if `visited_count == numCourses`.
* **Complexity:**
  * **Time:** $O(V + E)$ where $V$ is the number of courses (numCourses) and $E$ is the number of prerequisite pairs, as every unique node and directed edge is processed exactly once.
  * **Space:** $O(V + E)$ memory allocation footprint to house the explicit adjacency list blueprints inside memory alongside $O(V)$ auxiliary space for the indegree tracking registers.
* **Pointer Flow:**
```text
Dependency lock resolution for numCourses = 2, prerequisites = [[1, 0]]:
Directed Graph Arrow: 0 -> 1 (Course 0 must precede Course 1)
Initial State: adj = {0:, 1: []}, indegree =, visited_count = 0
queue = deque([0]) (Course 0 has zero prerequisite locks)

Loop Pass 1: Pop course 0 -> visited_count = 1. Unlocks downstream neighbor 1:
             indegree[1] -= 1 -> hits 0! -> Lock broken -> queue.append(1)
Loop Pass 2: Pop course 1 -> visited_count = 2. No outgoing edges. Loop closes.
Final Evaluation: visited_count (2) == numCourses (2) -> Returns TRUE.
```
* **Pattern Recognition:**
  - Use Kahn's BFS scheduling tracker when:
    - The problem asks whether a system of unidirectional constraints can be completed without getting trapped in a circular logical deadlock.
    - You want to detect a directed cycle cleanly using flat counter mechanics rather than managing recursive call stack colors.
* **Core Insight:** Kahn’s algorithm treats the entry queue as an execution pool for completely unlocked tasks. Vertices trapped inside a circular dependency cycle form a closed feedback ring; because no outside wave can break into the ring to clear those internal edges, their indegree counts can never reach 0. They stay trapped in memory, causing the final processed node count to fall short of the total vertex total, exposing the cycle instantly.

---

## Problem: Course Schedule II

* **Problem Type:** Complete Dependency Resolution / Topological Ordering Stream
* **Data Structure Used:** Adjacency List Map (`dict`) + Indegree Tracker Array (`list[int]`) + FIFO Queue (`collections.deque`)
* **Approach 1:** N/A
* **Optimized Approach:** Kahn's BFS Order Accumulator. Build the exact same incoming `indegree` mapping array and queue setup as Course Schedule I. Maintain a flat linear results list (`order`). As nodes are systematically popped from the front of the FIFO queue, immediately append their ID tokens directly into the `order` list before decrementing neighbor counters. If the final length of your order array matches the total course count (`len(order) == numCourses`), output the array; otherwise, return an empty list `[]`.
* **Complexity:**
  * **Time:** $O(V + E)$ linear time efficiency, ensuring optimal throughput across large task structures.
  * **Space:** $O(V + E)$ memory allocation footprint to store the structural graph networks alongside the output sequence blocks.
* **Pointer Flow:**
```text
Topological stream generation for numCourses = 4, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]:

Graph Structure:
0 -> 1 -> 3
 \        ^
  \      /
   -> 2 -

Adjacency List:
0 : [1, 2]
1 : [3]
2 : [3]
3 : []

Initial State:
indegree = [0, 1, 1, 2]
queue = deque([0])
order = []

------------------------------------------------------------

Pass 1:
Pop course 0
order = [0]

Process neighbors:
1: indegree[1] = 1 -> 0   (queue.append(1))
2: indegree[2] = 1 -> 0   (queue.append(2))

Current indegree = [0, 0, 0, 2]
Current queue = deque([1, 2])

------------------------------------------------------------

Pass 2:
Pop course 1
order = [0, 1]

Process neighbor:
3: indegree[3] = 2 -> 1

Current indegree = [0, 0, 0, 1]
Current queue = deque([2])

------------------------------------------------------------

Pass 3:
Pop course 2
order = [0, 1, 2]

Process neighbor:
3: indegree[3] = 1 -> 0   (queue.append(3))

Current indegree = [0, 0, 0, 0]
Current queue = deque([3])

------------------------------------------------------------

Pass 4:
Pop course 3
order = [0, 1, 2, 3]

No outgoing neighbors.

Current indegree = [0, 0, 0, 0]
Current queue = deque([])

------------------------------------------------------------

Final Evaluation:
len(order) = 4
numCourses = 4

Since len(order) == numCourses,
Return: [0, 1, 2, 3]
```
* **Pattern Recognition:**
  - Use Kahn's BFS order accumulator when:
    - The task requires outputting the literal chronological sequence or step-by-step roadmap that resolves a complex directed dependency tree.
    - Multiple valid sequence streams exist, and you want to extract them linearly from left to right without running manual array reversals.
* **Core Insight:** In a topological BFS run, a node is appended to the final results list only when it has been completely stripped of all incoming dependency locks. This means that if an edge exists from $u \rightarrow v$, $u$ is guaranteed to be drained and registered inside the output array long before $v$'s counter can ever reach 0, enforcing a flawless top-down chronological pipeline naturally.
* **Mistakes Made:** Forgetting to handle the failure state correctly when a cycle is detected. Returning a partially compiled, truncated `order` list instead of explicitly wiping out the array and returning an empty list `[]` allows corrupt, gridlocked schedules to escape into system pipelines, causing silent failures downstream.

---

## Problem: Alien Dictionary

* **Problem Type:** Lexicographical Character Sorting / String-Pair Edge Extraction Topological Sort
* **Data Structure Used:** Adjacency List Set Map (`dict` mapping `{str: set[str]}`) + Unique Key Indegree Tracker (`dict`)
* **Approach 1:** N/A
* **Optimized Approach:** String-Pair Edge Extraction paired with Kahn's Algorithm. Initialize an adjacency list map and an indegree map for *every single unique character* present across the word list. Run a lookahead loop comparing adjacent words pairwise (`word1` vs `word2`). Scan their character columns: the absolute first position where a character mismatch occurs (`word1[j] != word2[j]`) establishes a strict directed edge connection (`word1[j] -> word2[j]`). To prevent duplicate edge counting, verify that the edge doesn't already exist in the adjacency set before incrementing the neighbor's indegree. Immediately `break` out of the inner loop since subsequent letters in those words provide zero sorting context. Pipe this compiled character graph directly into Kahn's BFS engine.
* **Complexity:**
  * **Time:** $O(C)$ where $C$ is the total character length sum across all words in the input dictionary. Building the graph requires reading adjacent character sequences, and the topological sort runs over a fixed alphabet size capped tightly at a maximum constant of 26 characters ($O(V+E)$ → $O(26 + 26)$ = $O(1)$).
  * **Space:** $O(1)$ constant auxiliary workspace, since the unique keys inside the hash maps can never exceed the 26-letter English alphabet boundary footprint.
* **Pointer Flow:**
```text
Lexicographical edge extraction for words = ["wrt", "wrf", "er", "ett", "rftt"]:
Unique character mapping initialization: chars = {'w', 'r', 't', 'f', 'e'}

Pair 1: "wrt" vs "wrf"  -> mismatch at index 2: 't' != 'f' -> Edge: 't' -> 'f'
Pair 2: "wrf" vs "er"   -> mismatch at index 0: 'w' != 'e' -> Edge: 'w' -> 'e'
Pair 3: "er"  vs "ett"  -> mismatch at index 1: 'r' != 't' -> Edge: 'r' -> 't'
Pair 4: "ett" vs "rftt" -> mismatch at index 0: 'e' != 'r' -> Edge: 'e' -> 'r'

Compiled Character Graph: 'w' -> 'e' -> 'r' -> 't' -> 'f'
Kahn's sorting unrolls this sequence perfectly into output string: "wertf"
```
* **Prefix Edge Case Guard:** Before extracting edges, insert a crucial validation gate: if `word1` is strictly longer than `word2` and its starting prefix matches `word2` exactly (e.g., comparing `"apple"` vs `"app"`), **the dictionary layout is fundamentally invalid**. Return an empty string `""` immediately to fail-fast.
* **Pattern Recognition:**
  - Use string-pair edge extraction when:
    - You must derive a hidden, custom alphabetical sorting sequence or character precedence map from a pre-sorted list of text strings.
    - Character associations are implicit, requiring you to analyze structural layout mismatches to uncover directional constraints.
* **Core Insight:** Lexicographical sorting rules dictate that sorting order is settled at the absolute first character mismatch between two adjacent words. Every character after that mismatch contains zero priority context and must be completely ignored. Extracting these distinct unequal letter pairs and mapping them as directional graph edges transforms a messy text alignment problem into a clean, unweighted DAG topological sort.
* **Mistakes Made:** Forgetting to initialize the adjacency list keys and indegree counters for letters that never participate in a direct mismatch edge (e.g., a standalone letter like `'z'` that appears in the words but never clashes with its neighbors). If you only build map keys during edge insertions, these isolated characters will completely vanish from the tracking arrays, resulting in an incomplete alphabet output that corrupts the final dictionary string.

---

## Problem: Find Eventual Safe States

* **Problem Type:** Terminal-Bound Graph Inversion / Reverse Topological Sort
* **Data Structure Used:** Reversed Adjacency List Map (`dict`) + Indegree Tracker Array (`list[int]`) + FIFO Queue (`collections.deque`)
* **Approach 1:** Recursive DFS Cycle Detection with a recursion stack tracking set. Walk through every node; if it triggers a directed back-edge cycle, flag it as unsafe, while caching safe paths across deep tracks. While optimal, it requires careful management of three-state graph nodes during unrolling passes.
* **Optimized Approach:** Reverse Adjacency List Topological Sort (Sink-to-Source Propagation). Invert the problem paradigm completely: a node is mathematically "safe" if all paths leading from it terminate at a sink node (outdegree == 0). Build a **Reversed Adjacency List** (`rev_adj`) where edges point backward from destinations to sources, and let the `indegree` array track the *original outdegree* count of each node. Load all original sink nodes (`indegree == 0`) into the queue concurrently at Layer 0. Pop a terminal safe node, flag it `True` inside a global boolean array, and step backward across the reversed edge paths to decrement neighbor counters. When a neighbor's original outdegree drops to 0, it means all its outgoing paths can only navigate into verified safe zones—push it onto the queue.
* **Complexity:**
  * **Time:** $O(V + E)$ linear time footprint, as reversing edge arrays and running Kahn's loop sweeps every component exactly once.
  * **Space:** $O(V + E)$ memory footprint required to allocate the inverted adjacency tracking structures.
* **Pointer Flow:**
```text
Inverted distance-field mapping for graph = [[1, 2], [2, 3], [5], [0], [5], [], []]:
Initial State: original outdegrees compiled as indegree = [2, 2, 1, 1, 1, 0, 0]
Original sink nodes are 5 and 6. Queue = deque([5, 6]), safe = [False, False, False, False, False, False, False]

Pass 1: Pop node 5 -> safe[5] = True. Follow rev_adj backward to parent nodes 2 and 4:
        indegree[2] -= 1 -> hits 0! -> Lock broken -> queue.append(2)
        indegree[4] -= 1 -> hits 0! -> Lock broken -> queue.append(4)
Pass 2: Pop node 6 -> safe[6] = True. No incoming connections to 6.
Pass 3: Pop node 2 -> safe[2] = True. Follow rev_adj backward to parent node 0:
        indegree[0] -= 1 -> drops from 2 to 1 (Remains locked since it connects to unsafe node 1)...
```
* **Pattern Recognition:**
  - Use reverse adjacency topological sorting when:
    - The problem requires identifying elements whose paths are guaranteed to avoid directed loops or deadlock components completely.
    - The structural condition defines terminal "sink nodes" as the ultimate target destination milestones of the network graph.
* **Core Insight:** Reversing the graph's edge vectors turns terminal sink nodes into source anchors. Running Kahn's algorithm over an inverted network means the wave front radiates backward from known safe dead-ends toward the interior nodes. If a parent's original outdegree drops to 0, it serves as an absolute proof that *all* its original outward trajectories lead exclusively into safe, non-cyclic zones, allowing you to harvest safe states efficiently without running complex multi-pass lookahead searches.
* **Mistakes Made:** Forgetting that the final result list must be returned in strictly sorted ascending order. Kahn's algorithm pops nodes based on dependency breakdown sequencing, which outputs values in structural order rather than numerical order. Running a clean linear selection loop across the boolean array at the absolute end (`[i for i in range(n) if safe[i]]`) ensures the output layout complies with sorting constraints perfectly.

---

### Master Patterns Learned

#### 1. Zero-Dependency Indegree Draining (The Structural Selection Pool)
* **Applied to:** Course Schedule, Course Schedule II, Alien Dictionary
* **The Strategy:** Use this architectural template when a problem space requires resolving a complex web of mutual, one-way directed constraints (prerequisites, package tracking, build orders). By calculating an explicit `indegree` counter map to record exactly how many unresolved dependency locks each vertex holds, you can isolate all zero-lock source nodes up front. Processing elements exclusively through a FIFO queue ensures that task execution tracks move forward cleanly without recursive call overhead.
* **The Conceptual Mechanics:**
  - **Prerequisite Clock Decoupling:** Instead of wandering through graph layers blindly via full-depth explorations, Kahn's algorithm updates node availability dynamically on the fly. Decrementing a neighbor's counter (`indegree[neighbor] -= 1`) strips away a single dependency link; the absolute millisecond that register hits 0, the node is certified safe and injected into the active execution pool.
  - **Implicit Flow Deduplication:** Because a vertex can only cross the entry threshold of the queue if its incoming dependency weight is exactly 0, it is physically impossible for any node to undergo duplicate processing loops, protecting system runtimes from exponential performance bottlenecks.
* **The Layout / Code Pattern:**
```python
from collections import deque

def resolve_directed_dependency_tree(total_nodes: int, constraint_edges: list[list[int]]) -> list[int]:
    # Phase 1: Reconstruct raw pairs into an Adjacency List and compile Indegrees
    adj_map = {i: [] for i in range(total_nodes)}
    indegree_registry = {i: 0 for i in range(total_nodes)}
    
    for dependent_node, prerequisite_node in constraint_edges:
        # Structure Arrow: Prerequisite -> Dependent
        adj_map[prerequisite_node].append(dependent_node)
        indegree_registry[dependent_node] += 1
        
    # Phase 2: Seed the FIFO queue with all absolute dependency-free entry points
    active_selection_pool = deque([idx for idx in range(total_nodes) if indegree_registry[idx] == 0])
    chronological_output_sequence = []
    
    # Phase 3: Interleaved Draining Loop
    while active_selection_pool:
        current_task = active_selection_pool.popleft()
        chronological_output_sequence.append(current_task)
        
        for downstream_neighbor in adj_map[current_task]:
            indegree_registry[downstream_neighbor] -= 1         # Break a dependency lock
            
            if indegree_registry[downstream_neighbor] == 0:
                # Absolute last prerequisite cleared -> Move task to active execution pool
                active_selection_pool.append(downstream_neighbor)
                
    # Phase 4: Structural Gridlock Verification Gate (Implicit Cycle Detection)
    if len(chronological_output_sequence) != total_nodes:
        return []       # Cyclic gridlock detected! A valid sequence is mathematically impossible.
        
    return chronological_output_sequence
```

#### 2. Pairwise Mismatch Axis Extraction (The Character Precedence Mapping Frame)
* **Applied to:** Alien Dictionary
* **The Strategy:** Use this sophisticated lookup combination framework when a hidden chronological sorting sequence or precedence matrix must be decoded from a list of elements that are already sorted under a foreign layout rule (e.g., words sorted in an unknown alien alphabet). Run a lookahead scan to analyze the list pairwise. Compare columns line-by-line: the absolute first position where an element mismatch occurs defines a valid, directional graph edge connection. Break the column check immediately on that mismatch to preserve priority boundaries.
* **The Conceptual Mechanics:**
  - **Isolating Priority Anchors:** Lexicographical or alphabetical priority is entirely resolved at the first point of divergence between two adjacent strings. Once a letter mismatch establishes that Character A comes before Character B, all subsequent letters inside those specific strings carry zero relative sorting weight and must be skipped to avoid corrupting priority paths.
  - **Prefix Safety Filtering:** A shorter string must mathematically precede a longer string if their overlapping prefix regions match exactly (e.g., `"app"` comes before `"apple"`). If this geometric alignment is inverted inside the input data, the system rules are fundamentally broken, allowing an early-exit guard line to abort execution before spinning up the graph engines.
* **The Layout / Code Pattern:**
```python
def extract_precedence_graph(sorted_data_stream: list[str]) -> dict:
    # 1. Initialize data tracking structures for ALL unique token elements
    unique_tokens = set("".join(sorted_data_stream))
    adjacency_tree = {token: [] for token in unique_tokens}
    indegree_map = {token: 0 for token in unique_tokens}
    
    # 2. Pairwise Lookahead Sweep Pass
    for i in range(len(sorted_data_stream) - 1):
        item1 = sorted_data_stream[i]
        item2 = sorted_data_stream[i + 1]
        
        # Fast-Fail Prefix Guard: Invalid structural inversion check
        if len(item1) > len(item2) and item1.startswith(item2):
            return {}       # Critical system error: Abort graph generation
            
        # Scan character columns line-by-line
        min_length_boundary = min(len(item1), len(item2))
        for col in range(min_length_boundary):
            if item1[col] != item2[col]:
                # Absolute first point of structural divergence discovered!
                parent_token = item1[col]
                child_token = item2[col]
                
                if child_token not in adjacency_tree[parent_token]:
                    adjacency_tree[parent_token].append(child_token)
                    indegree_map[child_token] += 1
                    
                break       # Priority settled for this pair! Abort loop to block noise.
                
    return {"adj": adjacency_tree, "indegree": indegree_map}
```

#### 3. Reverse Adjacency Node Inversion (The Sink-to-Source Propagation Frame)
* **Applied to:** Find Eventual Safe States
* **The Strategy:** Use this advanced network paradigm when a directed graph problem requires identifying nodes whose outward trajectories are completely guaranteed to terminate safely inside specified "dead-end" boundaries or non-cyclic zones. Invert the problem landscape: construct a **Reversed Adjacency List** where edges run backward from destinations to sources, and re-map Kahn's tracking array to monitor the *original outdegree* weights. Seeding the initial queue with all original terminal sink nodes allows you to track and extract safe states backward in a single integrated pass.
* **The Conceptual Mechanics:**
  - **Inverted Outbreak Fields:** Reversing edge channels transforms static terminal dead-ends into active, zero-cost source nodes. The wave front radiates backward from known safe exits toward the interior nodes of the network graph.
  - **Upstream Safety Clearance:** Because a parent node can only clear its incoming queue gate if its remaining outdegree counter reaches exactly 0, it means *every single one of its original outgoing choices* has already been processed, drained, and certified as a safe pathway lane, pruning out cyclic or hazardous traps automatically.
* **The Layout / Code Pattern:**
```python
from collections import deque

def isolate_safe_terminal_states(graph_topology: list[list[int]]) -> list[int]:
    total_nodes = len(graph_topology)
    reversed_adjacency_tree = {i: [] for i in range(total_nodes)}
    original_outdegree_registry = [0] * total_nodes
    
    # Phase 1: Invert the network geometry and assign outdegree counts to tracking counters
    for source_node in range(total_nodes):
        for destination_node in graph_topology[source_node]:
            # Reverse edge link allocation: Destination points back to Source
            reversed_adjacency_tree[destination_node].append(source_node)
            original_outdegree_registry[source_node] += 1       # Track original out-going lines
            
    # Phase 2: Pre-populate the queue with ALL original terminal sink nodes (Outdegree == 0)
    safe_nodes_queue = deque([idx for idx in range(total_nodes) if original_outdegree_registry[idx] == 0])
    safe_status_mask = [False] * total_nodes
    
    # Phase 3: Upstream Extraction Pass
    while safe_nodes_queue:
        verified_safe_node = safe_nodes_queue.popleft()
        safe_status_mask[verified_safe_node] = True
        
        # Step backward along the inverted tracking channels
        for upstream_parent in reversed_adjacency_tree[verified_safe_node]:
            original_outdegree_registry[upstream_parent] -= 1       # Clear an outgoing vector link
            
            if original_outdegree_registry[upstream_parent] == 0:
                # ALL outgoing pathways from this parent are certified safe! Push to queue.
                safe_nodes_queue.append(upstream_parent)
                
    # Phase 4: Output collection sorted chronologically in ascending order
    return [i for i in range(total_nodes) if safe_status_mask[i]]
```