## Problem: Generate Parentheses

* Brute force: Generating every possible sequence of open and close brackets of length 2n using a combinatorial generator, and then validating each sequence from scratch with a linear balance-checking loop.
```python
import itertools

def generate_valid_parentheses(n):
    choice = ["(", ")"]
    raw_combinations = itertools.product(choice, repeat=2 * n)
    valid_list = []
    for s in raw_combinations:
        string = "".join(s)
        balance = 0
        is_valid = True
        for s in string:
            if s == "(":
                balance += 1
            elif s == ")":
                balance -= 1
            
            if balance < 0:
                is_valid = False
                break                 
        if is_valid and balance == 0:
            valid_list.append(string)
    return valid_list
```
* Optimized: Building strings character-by-character using backtracking recursion, applying strict conditional safety checks ahead of time to ensure only mathematically valid sequences are explored.
```python
def generate_parentheses_optimal(n):
    result = []
    def backtrack(current_string, open_count, close_count):
        if len(current_string) == 2 * n:
            result.append(current_string)
            return
        if open_count < n:
            backtrack(current_string + "(", open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current_string + ")", open_count, close_count + 1)
    backtrack("", 0, 0)
    return result
```
* Data structure used: Itertools products and temporary strings for brute force; A recursive execution call stack and a storage array for optimization.
* Complexity:
  * Brute Force: Time $O(n \cdot 4^n)$ because it evaluates all $2^{2n} = 4^n$ permutations and executes a validation loop of size $2n$ on each; Space $O(n \cdot C_n)$ to store the valid matching string outputs, where $C_n$ is the $n$-th Catalan number.
  * Optimized: Time $O(\frac{4^n}{n\sqrt{n}})$ bounded precisely by the $n$-th Catalan number since the algorithm only wanders down valid decision branches; Space $O(n)$ to account for the maximum call stack depth of the recursive memory frames.
* Mistakes made: Relying on string length caps with `<=` inside poorly bounded `while` loops allowed appending steps to overflow past execution walls, trapping the script in an infinite loop. Furthermore, executing random sample guessing capped by a hardcoded constant (`1000`) caused the logic to break mathematically for larger values of $n$ because it lacked the scope to reach the boundaries of the combination search space. Finally, attempting to reject an invalid string mid-loop using `continue` instead of `break` failed because it only skipped to the next character rather than stopping the validation process entirely.
* What I learned: Recursion acts like a systematic checklist of chores. When an `if` condition executes a recursive function call, it pauses the current execution frame in place and dives deeper, only resuming subsequent `if` checks once the upper levels hit a dead end and return. By enforcing predictive state boundaries (`open_count < n` and `close_count < open_count`), we create a non-overlapping geometric path that naturally explores every structural configuration exactly once, dropping the need for an external deduplication `set`.

---

## Problem: Daily Temperatures

* Brute force: Using nested loops where each day scans all subsequent days linearly until it finds a higher value, tracking the distance between their indices.
```python
def daily_temperatures(temperatures):
    output_list = [0] * len(temperatures)
    for i in range(len(temperatures)):
        for j in range(i + 1, len(temperatures)):
            if temperatures[j] > temperatures[i]:
                output_list[i] = j - i
                break
    return output_list
```
* Optimized: Iterating through the array while maintaining a monotonic decreasing stack that stores unresolved day indices, popping elements to calculate index deltas the moment a warmer temperature breaks the trend.
```python
def daily_temperatures_optimal(temperatures):
    n = len(temperatures)
    output_list = [0] * n
    stack = [] 
    
    for current_index, current_temp in enumerate(temperatures):
        while stack and current_temp > temperatures[stack[-1]]:
            past_index = stack.pop()
            output_list[past_index] = current_index - past_index
        stack.append(current_index)
        
    return output_list
```
* Data structure used: Nested arrays with a pre-allocated results array for brute force; A sequential list used as a monotonic tracking stack for optimization.
* Complexity:
  * Brute Force: Time \(O(n^2)\) because every element can potentially trigger a full remaining scan of the array; Space \(O(1)\) auxiliary space as calculations are written directly into the pre-allocated output array.
  * Optimized: Time \(O(n)\) since each day's index is pushed onto and popped from the stack at most once; Space \(O(n)\) to buffer unresolved indices inside the stack.
* Mistakes made: Looking ahead inside the sequence boundary via `temperatures[i+1]` without capping the execution range, causing an out-of-bounds pointer error at final index execution. Furthermore, using a global scalar incrementer (`count += 1`) fails to capture contextual window distances, mistakenly accumulating global frequencies rather than the targeted index offset delta.
* What I learned: Monotonic stacks are ideal for "next greater element" scenarios. Instead of searching forward into the future with a nested loop, you push the current index onto a stack and look *backward* to resolve past elements. The distance between indices (`j - i` or `current_index - past_index`) perfectly yields the elapsed day count without nested tracking loops.

---

## Problem: Car Fleet

* Brute force: Attempting to find structural groups by running math calculations down un-ordered index lists and comparing independent time blocks across nested pointer boundaries.
```python
# Unsorted index comparisons fail because they allow trailing cars to be evaluated ahead of leading bottleneck cars.
```
* Optimized: Sorting cars by their starting position in descending order (closest to target first), calculating the exact time required to reach the target, and using a stack to collapse trailing cars into a single fleet if their arrival time is less than or equal to the bottleneck car in front of them.
```python
def car_fleet(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)
    stack = []
    for pos, spd in cars:
        time = (target - pos) / spd
        stack.append(time)
        if len(stack) >= 2 and stack[-1] <= stack[-2]:
            stack.pop()    
    return len(stack)
```
* Data structure used: A zipped and sorted list of tuples `[(pos, speed)]` processed sequentially via a monotonic time tracking stack for optimization.
* Complexity:
  * Brute Force: Time $O(n^2)$ due to nested lookahead scans; Space $O(n)$ to hold position snapshots.
  * Optimized: Time $O(n \log n)$ because sorting the cars by position dominates the runtime, while the single-pass stack loop runs in linear $O(n)$ time; Space $O(n)$ to store the paired car data patterns and stack frames.
* Mistakes made: Using integer floor division (`//`) instead of standard float division (`/`), which drops crucial decimal parts and corrupts accurate collision tracking. Furthermore, omitting a position-based sorting layout allowed trailing cars to be evaluated ahead of leading bottlenecks. Finally, deploying a nested lookahead pointer check (`for j in range(i+1...)`) caused multi-car intersections to double-count individual elements, miscalculating group boundaries.
* What I learned: Cars cannot pass each other, meaning fleet boundaries are completely determined by spatial order. Sorting descending allows us to process the lead cars first. If a trailing car has a time value less than or equal to the fleet leader directly in front of it (`stack[-1] <= stack[-2]`), it is guaranteed to catch up and merge. Popping the faster trailing car off the stack naturally tracks the total unique fleets as the final length of the stack.