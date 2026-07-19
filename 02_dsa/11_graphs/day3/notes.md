# Graphs on Grids

## 1. Grid as a Graph

### Why a Matrix is a Graph
A 2D array or matrix layout can be modeled mathematically as an unweighted, structural graph network. Instead of processing nodes using explicit Adjacency Lists or database mappings, a matrix grid defines its connections implicitly through its physical spatial geometry. 

*   **Cells as Vertices:** Every independent coordinate cell `(r, c)` on the grid serves as an isolated node vertex housing a value or terrain type.
*   **Valid Neighbours:** Edges are defined by horizontal and vertical proximity. Neighbors are the adjacent coordinates immediately bordering the active focus cell.

### 4-Direction vs. 8-Direction Movement
*   **4-Directional Traversal:** Movement is restricted strictly to the cardinal compass points (Up, Down, Left, Right). A cell at position `(r, c)` can transition exclusively to:
    \[\{(r-1, c), (r+1, c), (r, c-1), (r, c+1)\}\]
*   **8-Directional Traversal:** Movement allows diagonal steps alongside cardinal jumps, expanding the local option pool to include all surrounding boundary walls:
    \[\{(r-1, c), (r+1, c), (r, c-1), (r, c+1), (r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)\}\]

### Boundary Checking
Unlike standard graphs where neighbor loops are safely bounded by pre-allocated adjacency arrays, a matrix grid allows pointer coordinates to step clean off the physical sheet. To prevent fatal system out-of-bounds crashes, every single neighbor node calculation must pass through an absolute spatial validation gate:
\[\text{isValid} = (0 \le r < \text{ROWS}) \land (0 \le c < \text{COLS})\]

### Visited Handling: Separate Matrix vs. In-Place Mutation
To block cyclic feedback loops on open terrain grids, cells must be tracked once visited. There are two primary strategies to achieve this:
1.  **Separate Visited Matrix / Set:** Allocating a secondary boolean 2D grid (`visited = [[False] * COLS for _ in range(ROWS)]`) or a coordinates hash set (`visited = set()`). This tracks state history cleanly without altering any of the source board parameters.
2.  **In-Place Modification (Zero-Allocation Shield):** Overwriting the character or integer value directly inside the input grid cell with a temporary sentinel marker (e.g., changing land `'1'` to water `'0'`, or dropping a temporary character wall `board[r][c] = '#'` [1]). This completely avoids allocating extra memory on the heap.

## DFS vs BFS on Grids

### Use DFS when your objective requires:
*   **Component Counting:** Sweeping the grid matrix sequentially to locate and completely sink/erase standalone connected landmass shapes.
*   **Island Size / Property Aggregation:** Executing postorder style bottom-up calculations to measure the exact surface area, resource density, or weight of a contiguous land block.
*   **Flood Fill Recoloring:** Cascading a single baseline color outward across matching adjacent pixels until a solid contrasting boundary wall is breached.
*   **Recursive Graph Exploration:** Navigating deep paths where you need to check full branch combinations or trace continuous non-overlapping routes effortlessly using the implicit call stack.

### Use BFS when your objective requires:
*   **Shortest Path Optimization:** Calculating the absolute minimum number of coordinate jumps or step transformations required to travel between two points on an unweighted matrix sheet.
*   **Minimum Distance Mapping:** Identifying exact spatial boundary cushions or radial depth counters moving away from specific structural elements.
*   **Nearest Source Isolation:** Freezing traversal paths early the very first time an expanding horizon frontier contacts an acceptable target coordinate node.
*   **Symmetric Wave Propagation:** Radiating outward uniformly across concentric coordinate layers like an expanding ripple to process pixels equidistant from an origin point.
*   **Rotting Oranges / Multi-Source Outbreaks:** Managing multi-source contamination loops where several separate origin hubs infect the grid frontier simultaneously.
*   **Walls and Gates / Distance Fields:** Computing full-grid step arrays to map out exactly how far every single open cell sits from the nearest accessible gateway.

---

## 2. Grid Traversal Template

### Direction Arrays (`dirs`)
Instead of copy-pasting four repetitive conditional blocks for each directional step, we encapsulate coordinate translations into a clean, unified **Direction Array**. Iterating over this layout lets a single concise loop calculate offsets smoothly:

```python
# Cardinal 4-Directions: (dr, dc) mappings for [Up, Down, Left, Right]
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
```

### DFS Grid Template
```python
def traverse_grid_dfs(grid: list[list[str]]):
    if not grid: return
    ROWS, COLS = len(grid), len(grid[0])
    
    def dfs(r, c):
        # 1. Base Case: Enforce aggressive fail-fast boundary and terrain filters
        if r < 0 or c < 0 or r >= ROWS or c >= COLS or grid[r][c] == "0":
            return
            
        # 2. In-Place Mutation: Overwrite cell to drop a visited shield
        grid[r][c] = "0" 
        
        # 3. Generic Neighbour Iteration using direction vectors
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dfs(r + dr, c + dc)         # Plunge deep into adjacent cardinal cells
            
    # Master loop sweeps the grid to trigger traversals
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "1":
                dfs(r, c)
```

### BFS Grid Template
```python
from collections import deque

def traverse_grid_bfs(grid: list[list[str]], start_r: int, start_c: int):
    ROWS, COLS = len(grid), len(grid[0])
    
    # BFS Rule: Lock down the visited state IMMEDIATELY upon queue insertion
    grid[start_r][start_c] = "0"
    queue = deque([(start_r, start_c)])
    
    while queue:
        r, c = queue.popleft()          # True O(1) constant-time pop
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            
            # Boundary Check + Terrain Validity Gate
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == "1":
                grid[nr][nc] = "0"          # Lock node down early to block duplicate entries
                queue.append((nr, nc))
```

---

## 3. Common Grid Patterns

### Flood Fill
Starting from a target seed pixel, explore outward to locate all connected coordinate slots matching the original cell's color value, and paint them with a newly selected shade. This pattern defines basic image coloring tools and area selection boundaries.

### Island Expansion / Size Aggregation
Run a traversal pass over a connected landmass component chunk, returning a scalar integer total representing the absolute surface area or sum total of all contiguous cells embedded inside that specific block.

### Component Counting
Run a master double-nested loop across every coordinate on the sheet. When a target terrain cell is breached, increment your global component tracker immediately, and launch an exhaustive DFS or BFS helper pass to completely wipe out or consume that entire connected island before control returns to the main loop counters.

### Boundary DFS
A highly optimized filtering technique where you run traversal helpers exclusively along the exterior perimeter borders of the matrix (the top row, bottom row, left column, and right column). This lets you identify and consume all cells safely connected to the outer world, isolating land-locked interior elements automatically.

### Multi-Source BFS
An advanced layer-by-level propagation strategy where *multiple separate origin points* are injected into a single global FIFO data queue concurrently right at startup. The wave front radiates outward from all source locations simultaneously, allowing you to calculate shortest path distance fields across wide environments efficiently.

---

## 4. Common Grid Mistakes

### Forgetting Boundary Checks
Failing to verify that `0 <= nr < ROWS` and `0 <= nc < COLS` before reading cell indices (`grid[nr][nc]`). This causes the pointer to drop off the sheet, immediately throwing an `IndexError` crash that breaks execution.

### Revisiting Cells (Missing / Late Visited Flags)
Waiting until an element is popped from a BFS queue to toggle its visited state. This introduces a dangerous time lag, allowing neighboring paths across the same row to observe the cell as unvisited and push multiple redundant duplicate copies of it into the queue array, causing memory usage to expand out of control.

### Incorrect Direction Vectors
Writing mismatched offset steps inside manual coordinate blocks (e.g., using `r + 1` paired with `c + 1` instead of cleanly decoupling them into orthogonal shifts). This silently corrupts the traversal engine, forcing the pointer to jump across diagonal cells when it should be stepping strictly along cardinal axes.

### Mixing Rows and Columns
Swapping index parameters inside matrix access bounds (e.g., using `grid[c][r]` instead of `grid[r][c]`). On non-square matrices where rows do not equal columns ($R \ne C$), this index reversal triggers immediate out-of-bounds segmentation crashes.

### DFS Stack Overflow on Massive Grids
Deploying deep recursive DFS sweeps on sprawling grid systems (e.g., a $1000 \times 1000$ matrix containing an massive all-land ocean path). This easily drives the recursive call frame count beyond Python's default system call ceiling threshold limit, ending in a fatal `RecursionError` crash. Massive open grids require switching the traversal code to an iterative, queue-based BFS loop.

### Mutating the Grid Unintentionally
Using in-place cell mutation tricks to optimize memory parameters when the parent problem demands preserving the original matrix data values completely uncorrupted for subsequent analysis paths. If preservation is mandatory, you must use a separate visited hash set or allocate a true reference clone copy of the board before starting.

---

---

## Problem: Flood Fill (DFS & BFS Comparison)

* **Problem Type:** Grid Color Propagation / Connected Component Flood Fill
* **Data Structure Used:** 2D Matrix Grid (`list[list[int]]`) / FIFO Queue (`collections.deque`)
* **Approach 1 (Recursive DFS):** Verify if `starting_color` already equals the target `color` to prevent infinite feedback loops. Launch a recursive DFS pass from `(sr, sc)`. At each coordinate, enforce boundary gates and check if the cell color matches the original shade. If it matches, overwrite the pixel value with the new color and plunge cardinally into its four adjacent neighbors.
* **Optimized Approach (Iterative BFS):** Initialize a `deque` pre-loaded with the `(sr, sc)` anchor coordinates. Overwrite the starting seed color immediately to seal the boundary early. While elements exist, pull the front coordinates using `.popleft()`. Sweep the cardinal direction vectors; if an adjacent neighbor sits within boundaries and matches the original color, paint it with the new color immediately and append it to the back of the queue.
* **Complexity:**
  * **Time:** $O(R \cdot C)$ for both variants, where $R$ is rows and $C$ is columns, as every single grid pixel is evaluated at most once.
  * **Space:** $O(R \cdot C)$ worst-case footprint. For DFS, this maps the call frame stack depth on a sprawling all-same-color grid; for BFS, this maps the peak width of the horizontal frontier queue buffer.
* **Pointer Flow:**
```text
Symmetric spatial recoloring across matrix image from coordinate (1, 1) with color = 2:
Image original values: -> starting_color = 1

Recursive DFS Traversal Path:
dfs(1, 1) -> image[1][1]=2 -> fires cardinally:
  ├── dfs(2, 1) -> matches original '1' -> image[2][1]=2 -> recurses downstream...
  └── dfs(0, 1) -> matches original '1' -> image[0][1]=2 -> recurses downstream...

Iterative BFS Wave Front:
queue = deque([(1, 1)]), image[1][1] = 2
Pop left (1, 1) -> looks cardinally:
  ├── neighbor (2, 1) -> matches '1' -> image[2][1]=2, queue.append((2, 1))
  └── neighbor (0, 1) -> matches '1' -> image[0][1]=2, queue.append((0, 1))
```
* **Pattern Recognition:**
  * Use grid color propagation when:
    - The problem requires modifying a continuous, contiguous block of identical terrain pixels starting from a single designated seed coordinate.
    - An immediate base case identity guard line (`if starting_color == color: return image`) can be used to prevent cyclic self-contamination.
* **Core Insight:** Flood fill models pixel replacement as graph reachability. Because the color mutation itself changes land value from the old shade to the new target shade, the updated cell value naturally functions as its own visited flag. This completely eliminates the need for any auxiliary hash sets or separate tracking matrices on the heap.
* **Mistakes Made:** Forgetting to place the identity guard check right at the entrance of the function. If you run a flood fill where the target color matches the starting color exactly, the conditional filter `image[r][c] != starting_color` will never evaluate to true, causing the algorithm to endlessly re-process the exact same cells, trapping the engine inside a fatal infinite recursion crash loop.

---

## Problem: Number of Islands

* **Problem Type:** Component Counting Sweep / In-Place Grid Sinking
* **Data Structure Used:** 2D Matrix Grid (`list[list[str]]`)
* **Approach 1:** Visited Set Coordinates Lookup. Driving a master double-nested loop across the grid. When land `'1'` is hit, add the coordinate tuple to a global hash set, increment your island counter, and run a standard traversal that cross-references all neighbor coordinates against the hash set on every step. This keeps the source array pristine but incurs an extra linear storage tax on the heap.
* **Optimized Approach:** In-Place Matrix Mutation (Grid Sinking Framework). Loop through every row $r$ and column $c$ on the board. When an unvisited land cell `'1'` is breached, increment your global `islands` counter immediately, and launch an exhaustive recursive DFS helper pass. The helper sweeps all four cardinal directions, aggressively sinking land values down to water (`board[r][c] = "0"`) inline, completely draining the entire connected component chunk before control returns to the master loop.
* **Complexity:**
  * **Time:** $O(R \cdot C)$ where $R, C$ are the board dimensions, since the master sweep reads every coordinate cell exactly once.
  * **Space:** $O(R \cdot C)$ worst-case auxiliary space matching the maximum recursive call frames stacked when traversing a massive all-land grid layout.
* **Pointer Flow:**
```text
Component extraction sweeps across matrix board =:
Outer Loops break land at coordinate (0, 0) == '1':
  ├── islands increments (0 -> 1)
  └── Launch dfs(0, 0) to completely sink the connected island component:
        ├── board[0][0] = '0' (Sunk!) -> fires cardinally
        ├── dfs(0, 1) -> land '1' found -> board[0][1] = '0' (Sunk!) -> recurses...
        └── dfs(1, 0) -> land '1' found -> board[1][0] = '0' (Sunk!) -> recurses...
Helper finishes and unrolls. Main loop loops to (0, 1) -> value is now '0' -> Skips cleanly!
```
* **Pattern Recognition:**
  * Use in-place matrix grid sinking when:
    - The objective asks you to calculate the total count of distinct, isolated clusters of land embedded within a background sea of water.
    - Mutating the input board characters directly is permitted, allowing you to wipe out explored territory to protect space efficiency.
* **Core Insight:** In-place mutation turns land cells into active visited shields. Sinking a land cell down to water (`"0"`) ensures that when the master outer nested loops advance to those exact coordinates on subsequent passes, the filter reads them as dead water blocks and skips over them instantly, completely avoiding redundant traversal calculations.
* **Mistakes Made:** The primary conceptual trap was misinterpreting the row and column boundaries inside the nested loop headers when handling non-square rectangular matrices. Writing `range(COLS)` inside the outer loop and `range(ROWS)` inside the inner loop instantly creates an index mismatch, triggering fatal out-of-bounds crashes.
* **What I Learned:** Driving component counts via master sweeps paired with inline grid sinking drops extra storage footprints down to zero. It ensures explored nodes are safely cleared from memory ahead of subsequent iterator checkpoints.

---

## Problem: Max Area of Island

* **Problem Type:** In-Place Value Aggregation / Bottom-Up Accumulation Grid DFS
* **Data Structure Used:** 2D Matrix Grid (`list[list[int]]`)
* **Approach 1:** Global Accumulator Class Pointer. Maintaining a standalone integer property `self.current_area = 0` inside the class space. During a land traversal sweep, increment this accumulator counter sequentially on every step, tracking maximum spans via a global check. While functional, it splits context away from the recursive return pipeline.
* **Optimized Approach:** Pure Bottom-Up Recursive Accumulation DFS. Drive a master double-nested loop across the board matrix. When land `1` is hit, call a recursive helper function that handles both land sinking and value collection concurrently. The helper checks boundaries: if a cell is water `0` or out of bounds, it returns a contribution value of `0`. If a cell is valid land, sink it to `0` immediately, and return a combined mathematical sum: `1 + dfs(Up) + dfs(Down) + dfs(Left) + dfs(Right)`. Track peak dimensions using a global maximum check (`max(max_area, dfs(r, c))`).
* **Complexity:**
  * **Time:** $O(R \cdot C)$ since each individual coordinate node is processed exactly once.
  * **Space:** $O(R \cdot C)$ auxiliary workspace corresponding to the deep recursive call stack frames.
* **Pointer Flow:**
```text
Bottom-up surface area aggregation passes over land cells:
Outer loop breaks land '1' at coordinate (0, 7):

dfs(0, 7) -> sinks board[0][7]=0 -> Returns: 1 + dfs(0, 8) + dfs(1, 7) + 0 + 0
  ├── dfs(0, 8) -> sinks board[0][8]=0 -> Returns: 1 + 0 + 0 + 0 + 0 = 1
  └── dfs(1, 7) -> water or empty boundaries -> Returns 0
Global Evaluation at root level: 1 + 1 + 0 + 0 + 0 = 2.
max_area updates: max(0, 2) = 2.
```
* **Pattern Recognition:**
  * Use bottom-up accumulation grid DFS when:
    - The problem requires calculating geometric properties (surface area, item weights, resource densities) of individual connected land components.
    - You need subproblems to calculate local sizes independently and bubble values back up the call stack to a parent root level.
* **Core Insight:** A land mass's total surface area is exactly equal to $1$ (the current cell) plus the combined surface area weights of its four adjacent cardinal branches. Forcing the helper function to return this mathematical sum directly allows sub-paths to execute independently and bubble their values back up, enabling the parent node to solve complex layout totals in true linear time.
* **Mistakes Made:** The hardest thought-driven hurdle was separating the return values of failed boundary lanes from valid paths. Accidentally returning a blank fallback or `None` on boundary failure checks instead of a clear numeric integer `0` (`if board[r][c] == 0: return 0`) breaks the accumulation math completely, throwing a `TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'` crash.
* **What I Learned:** Postorder styles are the ultimate tool for grid property aggregation questions. Bundling scalar arithmetic inside the return statements eliminates the need for separate tracking state registers.

---

## Problem: Island Perimeter

* **Problem Type:** Direct-Address Geometric Scanning / Linear Grid Cell Interlock Check
* **Data Structure Used:** None (Constant-Time Math Verification over Input Grid)
* **Approach 1:** Full Boundary DFS/BFS. Locate the island landmass, launch a full grid traversal pass, and increment a global perimeter counter by $1$ every single time an execution step hits a water cell or crosses a matrix boundary edge. This achieves the correct result but forces high call-stack spatial overhead ($O(R \cdot C)$ memory) to traverse the entire grid recursively.
* **Optimized Approach:** Direct-Address Linear Geometric Scanning. Run a direct double-nested traversal across the entire matrix. When a land cell `1` is encountered, add a full baseline of $+4$ to a global `perimeter` counter (assuming all 4 edges of the square are open to the water). Immediately check its top neighbor (`r > 0 and board[r-1][c] == 1`) and its left neighbor (`c > 0 and board[r][c-1] == 1`). For each active adjacent neighbor connection found, subtract exactly $-2$ from the global counter to account for the shared interlocking wall.
* **Complexity:**
  * **Time:** $O(R \cdot C)$ linear sweep time to inspect every coordinate block on the board exactly once.
  * **Space:** $O(1)$ constant workspace efficiency using zero extra memory allocations.
* **Pointer Flow:**
```text
Linear geometric interlocking checks for matrix cells:
Board = [,
    [1, 1, 1, 0]
]

1. Land cell found at (0, 1) -> perimeter += 4 (total=4). Checks top/left neighbors -> Empty.
2. Land cell found at (1, 0) -> perimeter += 4 (total=8). Checks top/left neighbors -> Empty.
3. Land cell found at (1, 1) -> perimeter += 4 (total=12).
   - Top neighbor at (0, 1) is 1! -> perimeter -= 2 (total=10)
   - Left neighbor at (1, 0) is 1! -> perimeter -= 2 (total=8)
```
* **Pattern Recognition:**
  * Use direct-address linear geometric scanning when:
    - The objective tracks static border perimeters or exterior boundary lengths across overlapping square matrices.
    - You want to eliminate the memory overhead of priority queues or recursive call frames entirely.
* **Core Insight:** Every standalone isolated square node possesses exactly $4$ open boundary sides. The absolute moment two square nodes touch and lock together, their shared wall disappears from the exterior perimeter list completely, reducing the total perimeter score by exactly $2$ sides ($1$ from each square). By checking only the *top* and *left* positions for every cell during a left-to-right, top-to-bottom matrix scan, you catch every interlocking connection exactly once, avoiding duplicate double-counting loops without running expensive recursive sweeps.
* **Mistakes Made:** Trying to check all four cardinal directions (Up, Down, Left, Right) inside the single cell block and subtracting $-1$ for each connection. While mathematically identical, checking all four sides requires complex lookahead boundary filters across all edges, which introduces high risk of duplicate double-counting operations unless you write messy coordinate restrictions. Looking strictly backward at top and left connections keeps the code short, safe, and clean.
* **What I Learned:** Recognizing geometric interlocking rules removes the need for active graph traversals entirely. Scanning backward boundaries allows the code to compute global perimeter layouts using simple, constant-space scalar subtraction.

---

### Master Patterns Learned

#### 1. In-Place Matrix Grid Sinking (The Zero-Memory Visited Eraser)
* **Applied to:** Number of Islands, Max Area of Island, Flood Fill
* **The Strategy:** Use this architectural template when a problem requires counting or aggregating properties across disconnected contiguous components embedded within a 2D matrix grid, and you are explicitly permitted to mutate the source data. Instead of allocating heavy auxiliary 2D boolean grids or coordinate hash tables on the heap, treat the input array itself as your primary workspace, mutating explored land cells directly down to water values inline to act as an unshakeable visited shield.
* **The Conceptual Mechanics:**
  - **Inline Threshold Erasure:** Overwriting a land block (`board[r][c] = "0"`) right at the entrance of a recursive frame destroys the candidate target value. When horizontal neighbor loops explore adjacent paths, or when the master outer sweeps advance across coordinates on subsequent passes, they read the cell as dead space and skip over it instantly, blocking duplicate processing steps.
  - **Memory Flattening Optimization:** Eliminating external tracking coordinate structures drops data allocation overhead from a heavy linear tax down to true constant O(1) auxiliary space parameters (excluding stack allocations).
* **The Layout / Code Pattern:**
```python
def in_place_grid_sinking_sweep(matrix_grid: list[list[str]]) -> int:
    if not matrix_grid: return 0
    ROWS, COLS = len(matrix_grid), len(matrix_grid[0])
    global_component_total = 0
    
    def sink_component_dfs(r, c):
        # 1. Fail-Fast Boundary & Terrain Verification Filters
        if r < 0 or c < 0 or r >= ROWS or c >= COLS or matrix_grid[r][c] == "0":
            return
            
        # 2. In-Place Mutation: Erase the land cell value to drop a visited shield
        matrix_grid[r][c] = "0"
        
        # 3. Cardinal Fanout Exploration
        sink_component_dfs(r + 1, c)
        sink_component_dfs(r - 1, c)
        sink_component_dfs(r, c + 1)
        sink_component_dfs(r, c - 1)

    # Master Nested Sweep: Scans the entire spatial grid sheet
    for r in range(ROWS):
        for c in range(COLS):
            if matrix_grid[r][c] == "1":
                global_component_total += 1         # New separate component breached!
                sink_component_dfs(r, c)            # Exhaustively erase the entire island mass
                
    return global_component_total
```
* **Recognition Signals / Triggers:**
  - Instructions requiring you to count **"Number of distinct islands"**, track **"Connected grid groups"**, or filter out separate clusters inside a 2D matrix layout.
  - Scenarios where mutating or overriding the source matrix characters is acceptable to optimize performance boundaries.

#### 2. Linear Interlocking Boundary Discounting (The Backward Lookahead Filter)
* **Applied to:** Island Perimeter
* **The Strategy:** Use this direct-address layout when your objective tracks static border lengths or exterior perimeter lengths across overlapping square matrices. Instead of running expensive recursive graph searches that consume high call stack frames, process the board linearly via a double-nested loop. Assume every land cell possesses a maximum open perimeter score, and check only backward-facing coordinates (top and left) to calculate and discount interlocking shared boundaries on the fly.
* **The Conceptual Mechanics:**
  - **Shared Boundary Elimination:** A single standalone box contains exactly 4 open perimeter faces. The absolute moment two boxes merge, their shared interlocking wall is hidden from the outside world entirely, reducing the total system perimeter count by exactly 2 open sides (1 side from each square component).
  - **Unidirectional Historical Scan:** Because a nested loop processes the grid sequentially from top-to-bottom and left-to-right, checking only the *top* and *left* borders for every active cell guarantees that you catch and verify every single interlocking connection exactly once. This completely eliminates duplicate double-counting calculations without requiring any track history hash maps.
* **The Layout / Code Pattern:**
```python
def static_grid_perimeter_calculator(matrix_grid: list[list[int]]) -> int:
    ROWS, COLS = len(matrix_grid), len(matrix_grid[0])
    global_perimeter_score = 0
    
    for r in range(ROWS):
        for c in range(COLS):
            if matrix_grid[r][c] == 1:
                # Step 1: Ingest max open capability boundaries up front
                global_perimeter_score += 4
                
                # Step 2: Unidirectional Historical Check: Look BACKWARD at top connection
                if r > 0 and matrix_grid[r - 1][c] == 1:
                    global_perimeter_score -= 2         # Deduct shared interlock wall
                    
                # Step 3: Unidirectional Historical Check: Look BACKWARD at left connection
                if c > 0 and matrix_grid[r][c - 1] == 1:
                    global_perimeter_score -= 2         # Deduct shared interlock wall
                    
    return global_perimeter_score
```
* **Recognition Signals / Triggers:**
  - Problem statements asking for **"Total island perimeter"**, **"Length of the grid boundary"**, or tracking exterior edges across overlapping components.
  - Matrix problems where you must evaluate boundary interfaces between different cell values without tracking paths dynamically.