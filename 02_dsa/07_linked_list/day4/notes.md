## Problem: LRU Cache

* **Problem Type:** In-place pointer modification / Cache eviction architectures (Least Recently Used Page Replacement Algorithm)
* **Data Structure Used:** Hash Map + Doubly Linked List (`dict` + custom `Node`)
* **Approach 1:** Maintaining a standard Python list or dictionary and updating a secondary array of timestamps on every read or write. This approach triggers slow O(n) operations during every single lookup or modification because it forces a linear scan to relocate keys or identify the oldest cache timestamp.
* **Optimized Approach:** Linking a Hash Map to a Doubly Linked List containing a pre-initialized `head` and `tail` dummy node system. The map enables instant lookup, while the doubly linked nodes allow you to safely isolate a node, snip its neighbors, and move it to the **Most Recently Used (MRU)** side of the doubly linked list (in our implementation, near `head`).
* **Complexity:**
  * **Time:** $O(1)$ constant time for both `get` and `put` actions.
  * **Space:** $O(capacity)$ ≈ O(n), where n is max cache size.
* **Pointer Flow:**
```text
State of nodes upon isolated update/insertion:
1. Isolate the target node (Snip references):
   node.prev.next = node.next
   node.next.prev = node.prev

2. Splice node directly at the front (Head connection):
   node.next = head.next
   node.prev = head
   head.next.prev = node
   head.next = node
```
* **Core Insight:** This system implements the **Least Recently Used (LRU) Page Replacement Algorithm**, a fundamental strategy used by Operating Systems to manage virtual memory paging and database buffers. A standard dictionary is unordered, while a singly linked list takes $O(n)$ time to delete nodes from the middle. By combining a map for $O(1)$ location with a doubly linked list for $O(1)$ extraction and splicing, you bypass the performance limits of both individual components, creating an exceptionally fast, self-contained data buffer that evicts the least recently used element from the tail in constant time.
* **Mistakes Made:** The primary conceptual trap was mismanaging boundary pointer links when a freshly updated node stood directly next to the dummy `head` or `tail` anchors. Forgetting to precisely stitch all four edge directions (`node.next`, `node.prev`, `head.next.prev`, and `head.next`) in exact chronological order was the hardest thought-driven bottleneck. Messing up this sequence instantly corrupts your memory references, creating a broken traversal path or completely dropping cache nodes.
* **What I Learned:** Complex cache structures require clear data decoupling. Using double dummy nodes (`head` and `tail`) creates a safe, fixed boundary cushion, completely dropping the need to check for null pointer values when evicting elements or adding nodes to an empty cache.

---

## Problem: Reverse Nodes in k-Group

* **Problem Type:** Multi-pass Traversal / Segment-wise In-place Reversal
* **Data Structure Used:** Singly Linked List
* **Approach 1:** Iterating through the chain to copy all node values or objects into a standard array, slicing the array into chunks of size `k`, flipping each valid subarray block manually, and then sewing the entire sequence back into a brand new linked list. This implementation takes $O(n)$ extra memory space.
* **Optimized Approach:** Run a sliding pointer loop to look ahead and verify if a complete window of size `k` remains (`kth`). If valid, isolate the block boundary, cleanly disconnect it from the trailing sub-list, execute a localized pointer reversal loop exactly `k` times, and then stitch the sub-list's entry and exit nodes back into the global tracking chain.
* **Complexity:**
  * **Time:** $O(n)$ linear traversal pass.
  * **Space:** $O(1)$ constant auxiliary memory space since modifications occur directly on existing pointer tracks.
* **Pointer Flow:**
```text
Setup chunk boundary markers before flipping:
group_prev -> [1 -> 2 -> 3] -> group_next

               |         |
             curr       kth

localized flip pass:
prev = group_next, curr = group_prev.next
Loop k times: nxt = curr.next; curr.next = prev; prev = curr; curr = nxt

After inversion (Stitch boundary walls back together):
temp = group_prev.next
group_prev.next = kth
group_prev = temp
```
* **Core Insight:** This problem extends the standard linked-list reversal pattern from “reverse entire list” to “reverse fixed-size segments while preserving global connectivity.” Reversing segments within a larger linked list requires precise node boundary caching. By saving reference pointers to the node directly preceding the window (`group_prev`) and the node sitting right after it (`group_next`) before executing an inversion loop, you create clear local anchor slots to securely re-attach the newly inverted sub-segment.
* **Mistakes Made:** The thought-driven challenge was managing boundary adjustments without accidentally creating an unintended circular loop or dropping trailing nodes. Figuring out how to properly advance `group_prev` right after an iteration phase was the hardest conceptual hurdle. Realizing that the original start of the chunk (`group_prev.next`) naturally rolls around to become the new trailing end of that group allows you to safely assign it as the next `group_prev` anchor marker for the upcoming pass.
* **What I Learned:** Multi-layered linked list manipulation requires strict separation of structural concerns. Breaking the execution flow down into explicit validation sweeps, isolated pointer inversions, and global boundary stitching steps prevents your pointers from losing context across deep structural jumps.

---

## Problem: Copy List with Random Pointer

* **Problem Type:** Structural Deep Cloning / Node Address Mapping (Graph Serialization / Deep vs Shallow Copy)
* **Data Structure Used:** Custom Linked Structure (next + random pointers) + Hash Map
* **Approach 1:** N/A
* **Optimized Approach:** Driven across a clean two-pass execution strategy. In the first pass, you parse the source list sequentially to copy each node's val directly into a fresh object allocation, storing the reference mapping `{original_node: copy_node}` inside a hash table. In the second pass, you traverse the list again, reading the map to instantly wire up the cloned node's `.next` and `.random` pointers in constant time.
* **Complexity:**
  * **Time:** $O(n)$ linear execution speed.
  * **Space:** $O(n)$ to house the original-to-cloned pointer tracking maps.
* **Pointer Flow:**
```text
Pass 1: Dictionary creation pass
mapping[curr] = Node(curr.val)

Pass 2: Structural lookup and pointer alignment
copy_node = mapping[curr]
copy_node.next = mapping.get(curr.next)       # Safe constant-time lookup
copy_node.random = mapping.get(curr.random)   # Handles random arbitrary links
```
* **Core Insight:** This problem tackles the architectural boundary of **Deep Cloning vs. Shallow Cloning** in graph structures. A shallow copy merely references the original node memory addresses, meaning modifications to the clone would dangerously corrupt or mutate the original list state. To achieve a true deep copy, we must duplicate the actual allocations on the heap. Standard object replication routines fail on complex cyclic networks because a node's random pointer can reference an arbitrary target that hasn't been instantiated yet. Separating individual node allocation from structural link assignment allows you to safely populate a global address book first, ensuring every pointer target can be securely retrieved and connected during the second pass.
* **Mistakes Made:** The main challenge was preventing runtime crashes when a node's `.next` or `.random` pointers evaluated to `None`. Utilizing standard dictionary bracket lookups like `mapping[curr.random]` will throw a `KeyError` on empty nodes. Switching the retrieval method to use `.get()` safely handles these scenarios by returning `None` instead of throwing a crash.
* **What I Learned:** Cloning structural memory address graphs requires building a reliable lookup reference map. Caching pointer targets inside a dictionary decouples memory creation from address linkage, transforming a complex graph cloning challenge into two clean, fast linear sweeps.

---

### Master Patterns Learned

#### 1. Composite Data Structure Linkage
* **Applied to:** LRU Cache
* **The Strategy:** High-performance architectural systems often link independent data shapes together to overcome individual layout bottlenecks. Combining an unordered Hash Map with a Doubly Linked List isolates key search paths down to $O(1)$ constant time, while unlocking instant node extractions and insertions in the middle of a continuous data stream.

#### 2. Segmented Boundary Synchronization
* **Applied to:** Reverse Nodes in k-Group
* **The Strategy:** In-place grid inversion across sub-ranges requires protecting the outer surrounding trail from breaking off in memory. By anchoring dedicated reference checkpoints (`group_prev` and `group_next`) directly outside the target window before running an iteration, you preserve a secure baseline grid map to cleanly stitch the inverted segments back together.

#### 3. Graph Address Mapping
* **Applied to:** Copy List with Random Pointer
* **The Strategy:** Replicating systems with non-linear or circular pointer dependencies requires separating object allocation from pointer wiring. Building a comprehensive dictionary lookup graph enables you to establish a robust reference map, allowing random cross-links to find their matching targets in constant time without deep traversal loops.

---

### Final Linked List Mental Models

#### 1. Mutation Near Head $\rightarrow$ Dummy Node Anchor
* **Trigger:** Deleting, inserting, or merging nodes where the initial `head` can be erased, mutated, or is unknown at startup.
* **Breakthrough:** Pre-pending a sentinel node (`dummy = ListNode(0, head)`) neutralizes head-specific edge cases, ensuring every real element can be processed uniformly using standard trailing pointer logic.

#### 2. Structural Midpoint or Loops $\rightarrow$ Tortoise & Hare (Slow/Fast)
* **Trigger:** Locating a center dividing line, finding a specific fraction of a list, or checking for internal circular paths.
* **Breakthrough:** Running two references at a 2:1 speed delta (`fast = fast.next.next` and `slow = slow.next`) forces the grid to partition itself geometrically, isolating midpoints or capturing cycle collisions in constant space.

#### 3. Spatial Segment Inversion $\rightarrow$ Pointer Reversal Trio (`prev-curr-nxt`)
* **Trigger:** Reversing a global list, flipping localized windows, or rearranging elements in reverse order.
* **Breakthrough:** Driving three sliding variables forward together allows you to safely cache the unvisited path (`nxt = curr.next`) before aggressively breaking the active connection to point backward (`curr.next = prev`).

#### 4. Instant Mid-Stream Deletion $\rightarrow$ Doubly Linked List Layout
* **Trigger:** Building high-performance memory buffers (like LRU Caches) where elements inside the stream must be evicted or re-arranged in true $O(1)$ time.
* **Breakthrough:** Storing structural references to both the preceding and following nodes enables you to completely bypass linear search sweeps, allowing elements to un-stitch and isolate themselves from their neighbors instantly.

#### 5. Arbitrary/Cyclic Cross-Links $\rightarrow$ Graph Deep-Cloning Hash Map
* **Trigger:** Replicating non-linear graphs or lists with random pointers where forward paths reference elements that do not exist yet on the heap.
* **Breakthrough:** Decoupling raw memory allocation from pointer assignment using an object-to-object dictionary lookup (`{original_node: copy_node}`) allows you to map out an entire systemic grid layout first, ensuring complex cross-links resolve instantly in a single subsequent pass.