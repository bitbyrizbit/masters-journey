## Problem: Implement Trie (Prefix Tree)

* **Problem Type:** Prefix Tree / String Routing
* **Data Structure Used:** Trie (`TrieNode` with a nested mapping dictionary `{str: TrieNode}`)
* **Approach 1:** Using a flat Hash Set (`set()`) to store whole strings. While lookup (`search`) is average-case $O(1)$ constant time step, checking if a prefix exists (`startsWith`) forces an expensive $O(n \cdot p)$ (where $n$ is total strings and $p$ is prefix length) as you must scan every stored word inside the collection from scratch and compare up to $p$. 
* **Optimized Approach:** Constructing a hierarchical character tree out of nested dictionary nodes. Inserting a word creates a sequential path of character references down the nodes, flipping a terminal `is_end` boolean marker to `True` at the final node. Prefix lookups can then cleanly glide straight down the pre-allocated characters trail in pure linear time.
* **Complexity:**
  * **Time:** $O(m)$ for all core operations (`insert`, `search`, `startsWith`), where $m$ is the length of the target string or prefix.
  * **Space:** $O(n \cdot m)$ worst-case heap allocation memory to buffer $n$ words of maximum length $m$ when they share zero overlapping character paths. In practice, space is often significantly smaller due to prefix sharing.
* **Pointer Flow:**
```text
State of nodes inside the Trie after inserting "apple":
root -> {'a': TrieNode}
          └── {'p': TrieNode}
                └── {'p': TrieNode}
                      └── {'l': TrieNode}
                            └── {'e': TrieNode (is_end=True)}

search("app")   -> Walks down 'a' -> 'p' -> 'p'. Target node exists but is_end == False. Returns False.
startsWith("app") -> Walks down 'a' -> 'p' -> 'p'. Path exists successfully. Returns True.
```
* **Pattern Recognition:**
  * Use a Trie architecture when:
    - The problem constraints require high-frequency lookups on prefixes or word match completions.
    - Storing full raw strings inside memory creates a massive data footprint that can be compacted via prefix sharing.
* **Core Insight:** A Trie completely decouples lookup time from the total number of words inside the dictionary. Whether your database holds 10 words or 10 million words, finding a string depends entirely on the character length of the query itself ($O(m)$), as you are simply riding a chain of pre-allocated nested memory map pointers directly to the destination node.
* **Mistakes Made:** The primary conceptual hurdle was choosing between using a fixed-size list array (`[None] * 26`) or a dynamic dictionary (`children = {}`) inside the `TrieNode` instantiation constructor. Realizing that a dictionary handles any arbitrary input alphabet character sets (uppercase, lowercase, symbols) seamlessly without requiring complex ASCII offset index arithmetic (`ord(char) - ord('a')`) was the vital design choice to keep code clean and bug-free.
* **What I Learned:** Prefix trees turn string parsing lookups into an explicit step-by-step path navigation route. Flagging the terminal boundary with a dedicated boolean marker (`is_end`) handles overlapping strings cleanly without losing track of short sub-words.

---

## Problem: Design Add and Search Words Data Structure

* **Problem Type:** Wildcard Pattern Matching / Backtracking Trie DFS
* **Data Structure Used:** Trie Tree (Merging tree tracking with recursive state buffers)
* **Approach 1:** N/A
* **Optimized Approach:** Combine standard Trie path routing loops with a backtracking Depth-First Search (DFS) function. When navigating standard characters, advance the tree pointer step-by-step down the children map. The absolute moment you encounter a dot wildcard (`.`), freeze execution, step outside the loop, and use an inner loop to recursively spawn recursive DFS branches down *every single available child path* in the current node map.
* **Complexity:**
  * **Time:** $O(m)$ for standard clear strings where $m$ is word size. For all-wildcard queries like `...`, execution speeds expand to $O(\Sigma^m)$ where $\Sigma$ represents the size of the node child character alphabet map.
    - Worst case: $O(b^m)$, where $b$ is average branching factor and $m$ is word length. For lowercase English letters, $b$ ≤ 26.
  * **Space:** $O(m)$ stack execution memory frames allocated to track deep wildcard branch expansions during backtracking recursion passes.
* **Pointer Flow:**
```text
Searching pattern ".ad" inside a Trie containing "bad", "dad", "mad":
root -> {'b': TrieNode, 'd': TrieNode, 'm': TrieNode}

Word index j=0, char = '.' -> Wildcard triggered!
  ├── Loop option 1: child 'b' -> dfs(j=1, node_b) -> looks for "ad" from here. Matches! Returns True.
  ├── (Other child options 'd' and 'm' short-circuit instantly since True bubble returned)
```
* **Pattern Recognition:**
  * Use a wildcard backtracking Trie when:
    - String pattern query lookups contain dynamic substitution tags or multi-choice wildcards.
    - You must validate multiple independent tree pathways concurrently to confirm structural match boundaries.
* **Core Insight:** Standard pointer routing loops break down on wildcards because a dot tag removes the explicit character map key. Branching out dynamically via a recursive backtracking routine allows you to fork the evaluation tree, validating every possible character lane in parallel and returning `True` the absolute moment any individual trail hits a valid `is_end` checkpoint.
* **Mistakes Made:** The hardest thought-driven hurdle was organizing the loop range index offset variable `j` when changing from iterative lookups to recursive checks inside the wildcard branch block. Accidentally starting the inner loop check from index `0` instead of propagating `i + 1` causes the recursive framework to loop on the same wildcard character endlessly, trapping the execution inside a massive stack-overflow infinite crash loop.
* **What I Learned:** Wildcards change a flat pointer traversal path into an exhaustive search graph. Using recursive index boundaries allows the engine to pause execution on wildcards and explore multiple alternative roads concurrently without dropping the general path context.

---

## Problem: Word Search II

* **Problem Type:** Grid Traversal Backtracking / Trie-Guided Backtracking DFS
* **Data Structure Used:** 2D Character Board Array + Prefix Tree Tracker
* **Approach 1:** Naive Grid Search. Iterating through each cell of the grid board, firing off a fresh standalone grid backtracking loop from every coordinate, and running string comparisons against all individual target words inside the collection array. This triggers an expensive $O(w \cdot r \cdot c \cdot 4^m)$ time crash because the grid is searched from scratch for every single word independently.
* **Optimized Approach:** Trie-Guided Board Backtracking. Flatten the entire target words list up front into a comprehensive Prefix Tree (`TrieNode`). Instead of searching for words on the board, search the board *through the guidelines of the Trie*. When a coordinate matches a top-level Trie child key, dive into a grid DFS loop, passing the corresponding Trie node down as a structural map filter. Prune steps instantly if the board cell character does not exist in the current node's children map. To optimize retrieval further, store the literal whole string right inside the leaf node (`node.word = w`) to bypass string concatenation, and actively pop dead leaf keys (`node.children.pop(char)`) to prune exhausted paths completely.
* **Complexity:**
  * **Time:** $O(r \cdot c \cdot 4^m)$ in worst case traversal, plus $O(total characters in words)$ for Trie construction, where $r$, $c$ are the dimensions of the board and $m$ is the maximum length of a word.
    *Note:* Practical runtime is usually much lower due to Trie pruning.
  * **Space:** $O(w \cdot m)$ heap footprint allocations required to compile the lookup Prefix Tree graph.
    - $O(total characters across all words)$ because shared prefixes reduce memory.
* **Pointer Flow:**
```text
Grid DFS guided by a Trie path tracking loop:
Board = [['o', 'a'],          Trie = root -> 'o' -> 'a' -> 't' -> 'h' (word="oath")
         ['e', 't']]

1. board[0][0] == 'o' -> exists in root.children. Fire dfs(0, 0, root).
2. board[0][0] marked to '#' (Visited). Node moves down to 'o' node.
3. Neighbors checked: board[0][1] == 'a' -> exists in current_node.children. Fire dfs(0, 1, node_o).
4. Matches propagate straight down until node.word is uncovered -> Appends "oath" to results.
5. In-place pruning cleanup step: if not current_node.children -> pop 'h', pop 't', etc., to avoid re-scanning.
```
* **Pattern Recognition:**
  * Use a Trie-guided grid backtracking pattern when:
    - You need to cross-reference an entire dictionary collection against a multi-directional spatial data grid simultaneously.
    - Standard independent path matching lookups generate high computational duplication overhead across intersecting cell boundaries.
* **Core Insight:** A prefix tree acts as a global directional dashboard during board explorations. Passing a Trie node reference down into a grid backtracking loop allows you to evaluate the potential viability of *all* words inside your database concurrently in constant time. If a board cell's neighbor doesn't match an active key in your current Trie layer, you can prune the branch immediately, pruning massive blocks of the grid's search space before wasting processing steps on a dead end.
* **Mistakes Made:** The absolute cognitive hurdle was preventing identical duplicate words from entering the final result list when multiple spatial grid paths resolve to the same text pattern. Initially, using an external collection structure like set(res) clears duplicates at final output but leaves performance gains on the table. Fixing this by caching the whole string on the leaf node (node.word) and explicitly setting it to None the absolute moment a match is logged (curr_node.word = None) provides an incredibly elegant, self-cleaning solution.
* **What I Learned:** Mutating tree structural states dynamically during graph runs delivers major performance wins. Wiping out matched text flags prevents duplicate processing, and popping exhausted leaf nodes (node.children.pop(char)) allows the algorithm to shave down the search grid on the fly, preventing redundant lookups entirely.

---

### Master Patterns Learned

#### 1. Prefix-Decoupled Node Routing (The Digital Search Map)
* **Applied to:** Implement Trie (Prefix Tree)
* **The Strategy:** Use this structural archetype when your system requires high-frequency lookups on overlapping string sequences or prefix validation constraints. By breaking entire words down into a chain of nested character node references, you completely decouple string search speeds from the total size of your database volume. 
* **The Conceptual Mechanics:**
  - **Namespace Optimization:** Standard database lookups scale linearly or logarithmically based on total stored collection values $(\(O(\log n)\))$. A Trie transforms data matching into basic coordinate path navigation, pinning execution time strictly down to the length of the incoming query string ($O(m)$) regardless of database scale.
  - **Boundary Flagging:** Overlapping sub-strings share a single consolidated pointer lane in memory. Distinguishing between a standalone word insertion and a shared intermediate prefix segment is achieved cleanly by introducing a dedicated terminal boolean marker (`is_end`) on the boundary edge nodes.
* **The Layout / Code Pattern:**
```python
class PrefixNode:
    def __init__(self):
        self.children = {}          # Dynamic direct-address character tracking map
        self.is_final = False

class PrefixTree:
    def __init__(self):
        self.root = PrefixNode()
        
    def add_token(self, token: str) -> None:
        cursor = self.root
        for character in token:
            if character not in cursor.children:
                cursor.children[character] = PrefixNode()
            cursor = cursor.children[character]
        cursor.is_final = True      # Seal the word boundary
```
* **Examples:** Autocomplete dropdown generators, dictionary spell-check engines, routing tables for IP addresses, or T9 predictive text messaging systems.

#### 2. Multi-Path Wildcard Backtracking (The Choice-Fork Divergence Frame)
* **Applied to:** Design Add and Search Words Data Structure
* **The Strategy:** Use this combination pattern when standard character-by-character tree lookups must tolerate uncertain elements or wildcard substitution formatting tags (`.`). When standard alphanumeric characters match, the path behaves as a linear loop step. The moment a wildcard tag hits, the logic splits into an iterative backtracking framework, forking the call stack to explore *every single active child path* in parallel.
* **The Conceptual Mechanics:**
  - **Loop-to-Recursion Handoff:** Standard iterative paths are highly efficient because they keep lookups memory-light. Introducing a recursive fallback wrapper allows the program to safely pivot into a multi-tier branch evaluation loop exclusive to instances of unknown input entries.
  - **Fail-Fast Parity:** When a wildcard tag forces the call stack to branch down multiple alternative roads simultaneously, chaining sub-returns through an inclusive boolean check guarantees that the absolute moment any single lane uncovers a valid path confirmation, the structural results bubble up immediately to exit the graph.
* **The Layout / Code Pattern:**
```python
def pattern_match_dfs(index: int, active_node: PrefixNode, target_pattern: str) -> bool:
    cursor = active_node
    
    for i in range(index, len(target_pattern)):
        char = target_pattern[i]
        
        if char == ".":
            # Wildcard constraint triggered: execute multi-branch exploration fork
            for matching_child in cursor.children.values():
                if pattern_match_dfs(i + 1, matching_child, target_pattern):
                    return True         # Bubble up confirmation instantly
            return False                # All avenues exhausted without a valid match boundary
        else:
            if char not in cursor.children:
                return False
            cursor = cursor.children[char]
            
    return cursor.is_final
```
* **Examples:** Regular expression (regex) matching engines, structural file-globbing systems, dictionary queries with missing character variables, or fuzzy-string lookup algorithms.

#### 3. Trie-Guided Grid Excision (The Active Graph Pruning Filter)
* **Applied to:** Word Search II
* **The Strategy:** Use this advanced hybrid structure when cross-referencing an entire dictionary database against a multi-directional spatial array or matrix grid layout. Instead of wastefully exploring grid vectors independently for individual words, run a single unified board backtracking scan that uses a compiled Prefix Tree as an active path filter. If a grid coordinate's neighbor does not exist as a valid child key in your current Trie layer, kill the branch instantly, cutting off huge blocks of the search space.
* **The Conceptual Mechanics:**
  - **Global Dashboard Guidance:** Passing a Trie node reference pointer down into a spatial matrix backtracking function converts a blind coordinates sweep into a structured lookup pass. The board exploration tracks parameters only as long as the prefix tree verifies that the character path is viable.
  - **Dynamic Branch Excision:** The ultimate optimization tier involves modifying the tree graph architecture in place during execution. Storing the whole string inside the leaf node (`node.word`) drops data concatenation costs entirely, while actively removing keys (`node.children.pop(char)`) when their child maps drop to empty acts as a self-cleaning filter that prevents future loops from wastefully re-scanning exhausted nodes.
* **The Layout / Code Pattern:**
```python
def matrix_backtrack_dfs(r: int, c: int, parent_trie_node: PrefixNode, board: list[list[str]]):
    char = board[r][c]
    current_trie_node = parent_trie_node.children[char]
    
    # 1. Direct Leaf Extraction: Bypass character assembly strings entirely
    if current_trie_node.word:
        append_to_results(current_trie_node.word)
        current_trie_node.word = None       # Prevent duplicate collection lookups
        
    board[r][c] = "#"  # Freeze tracking coordinates to avoid self-overlap
    
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if boundaries_valid(nr, nc) and board[nr][nc] in current_trie_node.children:
            # Trie guidelines confirm path is viable -> step forward down grid branch
            matrix_backtrack_dfs(nr, nc, current_trie_node, board)
            
    board[r][c] = char      # Unfreeze coordinate tracking state (Backtrack rollback)
    
    # 2. Dynamic Trie Pruning: Prune exhausted leaves to strip dead paths completely
    if not current_trie_node.children:
        parent_trie_node.children.pop(char)
```
* **Examples:** Grid boggle cross-link solvers, DNA genomic pattern match matrices, automated crossword grid validators, or spatial optical character recognition (OCR) dictionary engines.