# Linked List

### Core Syntax
```python 
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### Golden Rules
1. Always draw pointer movement on paper first.
2. Cache `.next` before mutating links.
3. Watch for `None` edge cases.
4. Use fast/slow pointers for:
   - middle
   - cycle detection
   - cycle entry
5. Dummy nodes simplify head-edge cases.

### Common Bugs
- Losing list after `curr.next = prev`
- Forgetting `while fast and fast.next`
- Infinite loops due to bad pointer updates

---

## Problem: Reverse Linked List

* **Problem Type:** In-place pointer reversal
* **Data Structure Used:** Singly Linked List
* **Approach 1:** Extra array / stack approach. Traverse list, store values, then rebuild reversed list. Simpler but wastes memory.
* **Optimized Approach:** Moving a sliding group of three independent tracking pointers (`prev`, `curr`, `nxt`) forward together in a single pass. At each element node, we decouple the forward link and rewire it to look backward at the previous node.
* **Complexity:**
  * **Time:** $O(n)$
  * **Space:** $O(1)$
* **Pointer Flow:**
```text
Before:
prev -> None
curr -> 1 -> 2 -> 3 -> 4 -> 5 -> None

Step mechanics per iteration:
nxt = curr.next        # 1. Bookmark the remaining unvisited trail
curr.next = prev       # 2. Break the link and point backwards
prev = curr            # 3. Slide the previous anchor forward
curr = nxt             # 4. Step the current pointer forward

After complete loop:
None <- 1 <- 2 <- 3 <- 4 <- 5 (prev points to new head)
```
* **Core Insight:** Pointer rewiring order is completely unforgiving. If `curr.next` is re-routed or altered before you cache a temporary reference to the remaining trail, the remainder of the list breaks off and becomes entirely inaccessible in memory.
* **Mistakes Made:** Initially assumed backward movement was possible in a singly linked list using something like `prev.prev`. Since nodes only store `.next`, backward traversal is impossible directly. The only workaround would be repeatedly traversing from the head to find the previous node, which would degrade runtime to $O(n²)$. This turns a simple 10,000-node task into 50 million operations.
* **What I Learned:** Linked list problems are almost entirely pointer-ordering challenges rather than complex mathematical data calculations. Shifting multi-pointer tracking units cleanly isolates independent mutations while maintaining a fast linear run speed.

---

## Problem: Middle of the Linked List

* **Problem Type:** Slow/Fast Pointer
* **Data Structure Used:** Singly Linked List
* **Approach 1:** Two-Pass Traversal. Loop through the list from head to end to count the total nodes. Divide the total by 2 to figure out the mathematical index offset, then reset a new pointer at the head and step through the range sequentially to retrieve the middle node.
* **Optimized Approach:** Utilizing two pointer references traveling at a relative speed delta. The slow pointer advances by exactly 1 node per iteration step, while the fast pointer runs ahead by exactly 2 nodes. The moment the fast pointer hits the boundary floor, the slow pointer automatically catches up to the exact midpoint.
* **Complexity:**
  * **Time:** $O(n)$
  * **Space:** $O(1)$
* **Pointer Flow:**
```text
Initialization:
slow = head
fast = head

Iterative Jump Loop:
while fast and fast.next:
    slow = slow.next          # Steps 1 node forward
    fast = fast.next.next     # Steps 2 nodes forward

Visual positioning on odd length:
Step 0: [S/F]1 -> 2 -> 3 -> 4 -> 5 -> None
Step 1: 1 -> [S]2 -> [F]3 -> 4 -> 5 -> None
Step 2: 1 -> 2 -> [S]3 -> 4 -> [F]5 -> None (Loop terminates; slow is middle)
```
* **Core Insight:** Let the geometry of the search domain split itself in half automatically. A fast pointer moving twice as fast as the slow pointer naturally partitions the list. When the fast pointer reaches the end, the slow pointer must be at the midpoint, eliminating the need for a second traversal.
* **Mistakes Made:** Miscalculating structural boundary offsets and trying to handle loops using incorrect breaks like `while counter == count`. Off-by-one errors while computing `count // 2`, especially on even-length lists, made manual counting unreliable.
* **What I Learned:** Shifting from manual tracker accumulation variables to multi-speed structural pointer strategies drops loop calculation parameters entirely. Verifying ahead of time that `fast` and `fast.next` are completely unlinked from null spaces prevents runtime crashes.

---

## Problem: Linked List Cycle Detection

* **Problem Type:** Cycle Detection
* **Data Structure Used:** Singly Linked List
* **Approach 1:** Visited Node Hash Set. Store node references in a `set()`. If a node appears again, a cycle exists.
* **Optimized Approach:** Deploying two index pointers inside a single execution stream without dynamic storage tracking lists. A slow pointer jumps by 1 node and a fast pointer jumps by 2 nodes; if a structural loop circuit exists, the fast pointer will circle back around and collide with the slow pointer from behind.
* **Complexity:**
  * **Time:** $O(n)$
  * **Space:** $O(1)$
* **Pointer Flow:**
```text
Initialization:
slow = head
fast = head

Traversal Check:
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True     # Pointer collision proves a cycle exists
return False
```
* **Core Insight:** Inside a cycle, the fast pointer moves $2$ nodes while the slow pointer moves $1$ node, so the fast pointer gains exactly $1$ node per iteration. This means the distance between them decreases by $1$ repeatedly, making collision mathematically inevitable if a cycle exists.
* **Mistakes Made:** Expecting a two-step jumping pointer to accidentally "leap over" or bypass a one-step pointer inside a circular running loop without triggering a direct match, leading to architectural hesitation due to a lack of confidence in the underlying pointer math.
* **What I Learned:** Trust the physics and mathematical rules that govern pointer speeds. If a structural cycle exists anywhere in the stream, an index collision is 100% mathematically guaranteed. Eliminating high-level hashing objects to manage detection purely via constant-space pointer loops drops auxiliary memory footprints completely down to zero.