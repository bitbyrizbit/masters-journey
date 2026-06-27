## Problem: Time Based Key-Value Store

* Brute force: Iterating backward through all historical records under a given key to sequentially scan for a timestamp less than or equal to the queried target time.
```python
def get_brute(key, timestamp):
    if key not in store: return ""
    # Scan backward from the most recent entries
    for t, val in reversed(store[key]):
        if t <= timestamp:
            return val
    return ""
```
* Optimized: Organizing entries chronologically inside a dictionary mapped to list arrays, and applying binary search to find the largest timestamp that is less than or equal to the target.
```python
store = {}

def set(key, value, timestamp):
    if key not in store:
        store[key] = []
    store[key].append([timestamp, value])

def get(key, timestamp):
    if key not in store:
        return ""
    pairs = store[key]
    left, right = 0, len(pairs) - 1
    res = ""
    while left <= right:
        mid = (left + right) // 2
        if pairs[mid][0] <= timestamp:
            res = pairs[mid][1]
            left = mid + 1
        else:
            right = mid - 1            
    return res
```
* Data structure used: Hash Map combined with an Array of lists (`{str: [[int, str]]}`) to preserve chronological entry structures for optimization.
* Complexity:
  * Brute Force: Time $O(n)$ where $n$ is the total historical logs stored under a single key; Space $O(1)$.
  * Optimized: Time $O(\log n)$ per `get` operation because historical entries are added chronologically and queried via binary search; Space $O(n)$ overall, where $n$ is the total number of set() operations across all keys. The `get()` operation is essentially a floor lookup: find the greatest timestamp `<= target timestamp`.
* Pattern Recognition:
  * Use binary search on dynamic arrays when:
    - Elements arrive in a strictly monotonic or sorted order (like automated increasing timestamps).
    - You need to perform a floor lookup (finding the closest matching valid entry on or below a specific query cutoff).
* Core Insight:
  Since the system specifications guarantee that timestamps arrive in strictly increasing order, the data automatically forms a sorted timeline. This allows binary search to step in, tracking a rolling fallback candidate `res = pairs[mid][1]` whenever a timestamp is safe, while shifting pointers forward to look for an even closer match.
* Mistakes made: The primary cognitive hurdle was ensuring that the retrieval function handles cases where a target timestamp falls between two records or sits past the end of the timeline. Figuring out how to cache the last valid downward option (`res = pairs[mid][1]`) before moving the lower boundary forward was the vital breakthrough, ensuring the algorithm never drops historical tracking data when the exact timestamp is missing.
* What I learned: Binary search is perfect for building historical range query systems. Tracking a continuous fallback candidate variable allows the logic to safely settle on the closest past value without breaking down on precise fractional gaps.

---

## Problem: Median of Two Sorted Arrays

* Brute force: Merging both sorted input lists into a single consolidated array using a two-pointer merge routine, and extracting the median index directly from the newly created array.
```python
def findMedianSortedArrays_brute(nums1, nums2):
    merged = sorted(nums1 + nums2) # Simplest approach
    n = len(merged)
    if n % 2 == 0:
        return (merged[n//2 - 1] + merged[n//2]) / 2.0
    return float(merged[n//2])
```
* Optimized: Running binary search exclusively on the shorter array to locate a precise partition index that splits the combined elements into identical left and right halves, verifying boundary conditions in constant time.
```python
def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    x, y = len(nums1), len(nums2)
    left, right = 0, x
    
    while left <= right:
        partitionX = (left + right) // 2
        partitionY = (x + y + 1) // 2 - partitionX
        
        maxLeftX = nums1[partitionX - 1] if partitionX > 0 else float('-inf')
        minRightX = nums1[partitionX] if partitionX < x else float('inf')
        
        maxLeftY = nums2[partitionY - 1] if partitionY > 0 else float('-inf')
        minRightY = nums2[partitionY] if partitionY < y else float('inf')
        
        if maxLeftX <= minRightY and maxLeftY <= minRightX:
            if (x + y) % 2 == 0:
                return (max(maxLeftX, maxLeftY) + min(minRightX, minRightY)) / 2.0
            else:
                return float(max(maxLeftX, maxLeftY))
        elif maxLeftX > minRightY:
            right = partitionX - 1
        else:
            left = partitionX + 1
```
* Data structure used: None; index trackers (`int`) and floating boundary flags are used exclusively.
* Complexity:
  * Brute Force: Time $O((x + y)\log(x + y))$ due to sorting the merged array; Space $O(x + y)$ to build the new combined list structure.
  * Optimized: Time $O(\log(\min(x, y)))$ because binary search is isolated strictly to the smaller array; Space $O(1)$ constant auxiliary memory.
* Pattern Recognition:
  * Use binary search partitioning when:
    - You need to achieve sub-linear time efficiency across multiple independent sorted arrays.
    - The problem can be solved by finding a perfect, balanced split point across two disjoint datasets.
* Core Insight:
  Finding the median is mathematically identical to cutting two arrays into two halves such that every element on the left side is less than or equal to every element on the right side. By forcing the partition of the longer array to depend directly on the shorter one (`partitionY = (x + y + 1) // 2 - partitionX`), we only need to search one array to find the balanced boundary spot.
* Mistakes made: The thought-driven bottleneck was handling boundary edge cases where a partition falls entirely outside an array's length (such as an empty list `nums1 = []`). Realizing how to substitute these blank slots dynamically using negative infinity (`float('-inf')`) for the left wall and positive infinity (`float('inf')`) for the right wall was the hardest challenge, as it keeps the boundary comparisons safe from out-of-bounds pointer crashes. Another major hurdle was understanding *why the partition condition works at all* - the correct partition is reached only when both left partitions are less than or equal to the opposite right partitions.
* What I learned: Ensuring that binary search runs on the shorter array is mandatory to prevent negative index calculation errors on `partitionY`. Using infinity values as fallback safety nets keeps code clean and robust when handling empty arrays or lopsided data splits.

---

## Problem: Search a 2D Matrix

* Brute force: Iterating through every single cell of the matrix row by row and column by column until the target value is found or all coordinates are exhausted.
```python
def searchMatrix_brute(matrix, target):
    for row in matrix:
        if target in row: # Linear search across matrix rows
            return True
    return False
```
* Optimized: Treating the entire 2D grid as a single continuous 1D sorted array, mapping the midpoint pointer back to virtual row and column coordinates in constant time using division and modulo operators.
```python
def searchMatrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    rows = len(matrix)
    cols = len(matrix[0])
    left, right = 0, (rows * cols) - 1
    while left <= right:
        mid = (left + right) // 2
        mid_val = matrix[mid // cols][mid % cols]
        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    return False
```
* Data structure used: None; row, column, and cell coordinate calculations are managed entirely via scalar index tracking variables.
* Complexity:
  * Brute Force: Time $O(m \cdot n)$ where $m$ is rows and $n$ is columns; Space $O(1)$.
  * Optimized: Time $O(\log(m \cdot n))$ because the entire grid is searched in a single global logarithmic pass; Space $O(1)$ constant workspace footprint.
* Pattern Recognition:
  * Use virtual matrix unrolling when:
    - Each row is sorted
    - First element of row i > last element of row i−1
* Core Insight:
  Since the rows of the matrix are glued together in a perfectly sorted chain, the 2D grid can be viewed as a flattened 1D array. A virtual index `mid` can be unrolled back into a standard matrix location at any moment: `mid // cols` isolates the exact row index, while `mid % cols` targets the clean column offset.
* Mistakes made: The primary cognitive challenge was avoiding the temptation to write two separate binary search routines—one to isolate the row and another to search the column. Simplifying the problem down to a single global 1D index space `(rows * cols) - 1` removed all nested loop tracking complexity, but required precise mapping calculations to keep index lookups bug-free.
* What I learned: Modulo arithmetic (`mid % cols`) and floor division (`mid // cols`) are incredibly powerful tools for coordinate space flattening. They allow a standard 1D binary search loop to glide through multidimensional arrays without requiring any extra list data reallocation steps.