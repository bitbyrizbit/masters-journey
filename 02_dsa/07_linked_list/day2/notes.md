## Dummy Node Pattern
```python
dummy = ListNode(0)
dummy.next = head
```
* **Use when:**
  - Deleting elements or removing specific target nodes.
  - Merging, sorting, or reordering separate linked lists.
  - Handling edge cases where the initial `head` node itself might be mutated or erased.
* **Benefits:**
  - Avoids writing complex, special-case condition checks specifically for the `head`.
  - Simplifies pointer rewiring by ensuring a guaranteed, stable node always exists before the active list range.
* **Common Bugs:**
  - Losing list after `curr.next = prev`
  - Forgetting `while fast and fast.next`
  - Infinite loops due to bad pointer updates
  - Forgetting to detach halves before merge (`slow.next = None`)
---

## Problem: Merge Two Sorted Lists

* **Problem Type:** Dummy Node Merge
* **Data Structure Used:** Singly Linked List
* **Approach 1:** Generating a completely new array, iterating through both linked lists to append all values to it, sorting the array, and then reconstructing a brand new linked list from scratch. This takes $O(n \log n)$ time and $O(n)$ extra space.
* **Optimized Approach:** Splice the existing nodes together in-place by maintaining a `dummy` starter node and a traveling `tail` pointer. We compare the heads of both lists, attach the smaller node to our `tail.next`, step that list's pointer forward, and advance the `tail`.
* **Complexity:**
  * **Time:** $O(n + m)$ where n and m are the lengths of the two lists.
  * **Space:** $O(1)$ constant space since we only rewire existing pointer addresses.
* **Pointer Flow:**
```text
Initialization:
dummy = ListNode(0)
tail = dummy

While head1 and head2 are both not None:
If head1.val <= head2.val:        
    tail.next = head1
    head1 = head1.next
Else:
    tail.next = head2
    head2 = head2.next
tail = tail.next
```
*Note:* Using <= instead of < preserves stable ordering when equal values appear in both lists.

```text 
At Loop Exit (Stitch remainder):
tail.next = head1 if head1 else head2
```
* **Core Insight:** A `dummy` node is a life-saver for structural list building. It gives you a concrete, unshakeable anchor point to start attaching nodes to without needing complex, messy condition checks to determine if the "head" of your new list has been assigned yet.
* **Mistakes Made:** The primary conceptual hurdle here was figuring out how to handle leftover nodes when one list runs dry before the other. Initially, I thought about spinning up another loop to process the remainder, but because the inputs are already sorted, you can cleanly stitch the entire remaining trail to the tail in a single assignment: `tail.next = head1 if head1 else head2`.
* **What I Learned:** Linking lists together is about redirecting existing pointers, not creating new node allocations. Using a dummy node keeps edge cases uniform and allows the code to easily transition from iterative comparison loops to a clean final stitch step.

---

## Problem: Remove Nth Node From End of List

* **Problem Type:** Slow/Fast Pointer + Dummy Node
* **Data Structure Used:** Singly Linked List
* **Approach 1:** Two-Pass Method. Traverse the entire list once from head to end to calculate the absolute count of nodes. Calculate the target index from the front via `count - n`, then reset a tracking pointer at the head and loop forward to delete the target node.
* **Optimized Approach:** Create a `dummy` node pointing to the head, and position both a `fast` and `slow` pointer there. Advance the `fast` pointer forward by exactly `n + 1` steps. Then, move both pointers forward at the exact same pace. The moment `fast` lands on `None`, `slow` will be sitting precisely on the node *just before* the one that needs deletion.
* **Complexity:**
  * **Time:** $O(n)$ single-pass execution.
  * **Space:** $O(1)$ constant memory layout.
* **Pointer Flow:**
```text
Setup: dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None, n = 2
fast = dummy, slow = dummy

Step 1: Move fast ahead by n + 1 (3 steps)
dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
[S]                [F]

Step 2: Advance both together until fast is None
dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None -> None
                   [S]                     [F]

Step 3: Rewire next link to delete the node
slow.next = slow.next.next (Removes 4)
```
* **Core Insight:** To remove the n-th node from the end in a single pass, we can use a constant spatial offset. By forcing the `fast` pointer to maintain a gap of exactly n nodes ahead of `slow`, the moment `fast` hits the end boundary, `slow` is perfectly positioned to execute the surgical bypass deletion on its target neighbor.
* **Mistakes Made:** A major hidden trap is trying to delete the first node of the list when n equals the exact length of the chain. If you attach pointers directly to the `head`, the `slow` pointer will have nowhere to stand to execute the deletion. Initializing both pointers at a pre-pended `dummy` node shields the logic from this edge case completely, ensuring you always have a safe boundary cushion.
* **What I Learned:** Dummy nodes paired with dynamic index-offset pointers can solve single-pass deletion problems effortlessly. The dummy node guarantees that the head node can be wiped out using the exact same code structure as any middle node in the list.

---

## Problem: Reorder List

* **Problem Type:** Multi-pass Traversal + Slow/Fast Pointer + Pointer Reversal + In-place Rewiring
* **Data Structure Used:** Singly Linked List
* **Approach 1:** Copying all node references or data values into a standard Python list, then reconnect nodes in order (`0, n-1, 1, n-2, ...`). This takes O(n) extra space.
* **Optimized Approach:** Split the problem into three logical, independent operations. First, use a slow/fast pointer pair to locate the exact midpoint and sever the list into two halves. Second, execute an in-place pointer reversal on the entire second half. Third, weave the two halves together sequentially by alternating links using temporary variable registers.
* **Complexity:**
  * **Time:** $O(n)$ because midpoint search, reversal, and merge each traverse the list at most once.
  * **Space:** $O(1)$ constant memory footprint since all modifications happen in-place.
* **Pointer Flow:**
```text
Step 1: Locate midpoint and split
1 -> 2 -> 3 -> None  and  4 -> 5 -> None

After locating midpoint, break the list using:
slow.next = None

Step 2: Reverse the second half
second = 5 -> 4 -> None

Step 3: Interleave pointers using temp snapshots (temp1, temp2)
first = 1 -> 2 -> 3 -> None
second = 5 -> 4 -> None

temp1 = first.next, temp2 = second.next
first.next = second
second.next = temp1
first = temp1, second = temp2
```
* **Core Insight:** Complex linked list behaviors can often be broken down into simpler, smaller components. Instead of trying to invent a complex interleaving algorithm on a raw list, splitting the chain, flipping the back half, and weaving them together transforms a massive hurdle into three highly manageable foundational steps.
* **Mistakes Made:** The primary cognitive challenge was managing pointer state mutations during the final interleaving weave phase. It's incredibly easy to accidentally create a circular pointer loop or completely drop a trailing sub-list in memory. Realizing that you must use *two independent temporary variables* (`temp1 = first.next` and `temp2 = second.next`) to snapshot the unvisited paths of both lists before modifying any `.next` pointers was the hardest thought-driven breakthrough.
* **What I Learned:** In-place list interleaving requires meticulous pointer coordination. Grouping problems into discrete steps—midpoint detection, string reversal, and twin-track weaving—makes it easy to preserve linear execution speeds and constant space efficiency.