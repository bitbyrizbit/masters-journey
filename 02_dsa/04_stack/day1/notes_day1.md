## Problem: Valid Parentheses

* Brute force: Repeatedly replacing valid adjacent bracket pairs (`"()"`, `"[]"`, `"{}"`) with an empty string until no more replacements can be made, then checking if the string is empty.
```python
def valid_parentheses_brute(s):
    s = s.replace(" ", "")
    old_length = -1
    while len(s) != old_length:
        old_length = len(s)
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return len(s) == 0
```
* Optimized: Iterating through the string linearly, pulling the top character off a stack when a closing bracket hits, and concatenating them into a string to verify membership against a valid pairs list.
```python
def valid_parentheses(s):
    stack = []
    pairs = ["()", "[]", "{}"]
    
    for i in s:
        if i == " ":
            continue
        if i in ("(", "[", "{"):
            stack.append(i)
        elif i in (")", "]", "}"):
            if not stack:
                return False
            parentheses = stack.pop()
            parentheses += i 
            if parentheses not in pairs:
                return False 
        else:
            return False
    return len(stack) == 0  
```
* Data structure used: String replacements for brute force; Python Lists (`list`) for bracket storage, pair definitions, and sequential stack execution for optimization.
* Complexity:
  * Brute Force: Time (O(N^2)) because `.replace()` scans the string fully on each iteration of the loop; Space (O(N)) to generate replacement string copies.
  * Optimized: Time (O(N)) since the string is traversed in a single pass; Space (O(N)) to store unclosed elements in the stack buffer.
* Mistakes made: Peeking at the stack using `stack[-1]` and concatenating it with string properties without actively removing it from the tracking array via `.pop()`. This left historical elements on the stack, causing an `IndexError` on nested elements like `(())` and masking unclosed elements. Additionally, returning `True` blindly at the end of the loop without verifying `len(stack) == 0` allowed strings with mismatched dangling tags like `{ }]` to falsely pass verification. Furthermore, I completely missed handling edge cases where a closing bracket lands at the absolute start of the string (e.g., `"]"`), which originally led to out-of-bounds pointer crashes before adding the safety balance check `if not stack: return False`.
* What I learned: Stacks operate on a strict Last-In, First-Out (LIFO) removal pipeline. When evaluating pairs via string concatenation, you must pop the target out of the list completely to allow outer structural scopes to contract properly. Ensuring the tracking list is fully empty at final execution is mandatory to prove that every opened container found its match.

---

## Problem: Min Stack

* Brute force: Implementing a standard array wrapper where extracting the minimum value requires scanning the entire list linearly using Python's built-in `min()` function.
```python
class MinStackBrute:
    def __init__(self):
        self.stack = []
    def push(self, val: int) -> None:
        self.stack.append(val)
    def pop(self) -> None:
        self.stack.pop()
    def top(self) -> int:
        return self.stack[-1]
    def getMin(self) -> int:
        return min(self.stack)     # Expensive O(N) lookup
```
* Optimized: Using a parallel synchronization model where each item pushed is paired alongside the absolute minimum value observed up to that point in history inside a single tracking data stack.
```python
class MinStack:
    def __init__(self):
        self.stack = []     # Stores pairs of [val, current_min]

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append([val, val])
        else:
            current_min = min(val, self.stack[-1][1])
            self.stack.append([val, current_min])

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
```
* Data structure used: Standard Python List (`list`) mapping individual records for brute force; A stack of pairs [value, min_so_far] for optimization.
* Complexity:
  * Brute Force: Time (O(N)) for `getMin()` and (O(1)) for all other functions; Space (O(N)) overall.
  * Optimized: Time (O(1)) constant runtime across all operational constraints; Space (O(N)) to buffer state history trackers.
* Mistakes made: Forgetting to explicitly use the mandatory `self` variable parameter inside custom class function scope declarations. This omitted proper instance tracking records, breaking class-level attribute data assignments and blocking state changes completely.
* What I learned: Class methods require `self` to access instance attributes. It references the current object instance and allows methods to access or modify its attributes. Snapshotting the localized minimum state directly alongside incoming values during creation allows us to completely drop the need for looping lookups later down the line. Thus, by storing each value with the minimum seen so far, getMin() becomes O(1).

---

## Problem: Evaluate Reverse Polish Notation (Postfix)

* Brute force: Scanning the string array from the beginning repeatedly to locate operators, manually resolving the adjacent preceding pair values, and mutating the original list array space until one final scalar remains.
*Note:* This brute-force implementation is conceptual and not fully robust due to index shifts caused by in-place pops.
```python
def eval_postfix_brute(tokens):
    tokens_copy = tokens.copy()
    i = 0
    while len(tokens_copy) > 1:
        if tokens_copy[i] in ("+", "-", "*", "/"):
            n1 = tokens_copy.pop(i - 1)
            n2 = tokens_copy.pop(i - 2)
            # Evaluate using string arithmetic matching criteria
            expression = f"int({n2}) {tokens_copy[i-2]} int({n1})"
            res = int(eval(expression))
            tokens_copy[i - 2] = str(res)
            i -= 2
        i += 1
    return int(tokens_copy[0])
```
* Optimized: Traversing the inputs sequentially in a single pass while using a linear stack array to hoard raw integer variables, instantly stripping the top two elements out to resolve operations when an arithmetic symbol is triggered.
```python
def eval_postfix(tokens):
    operand_list = []
    for i in range(len(tokens)):
        # Robust validation path matching positive or negative integer characters
        if tokens[i].isdigit() or (tokens[i].startswith('-') and tokens[i][1:].isdigit()):
            operand_list.append(tokens[i])
        elif not tokens[i].isalnum():
            n1 = int(operand_list.pop())
            n2 = int(operand_list.pop())
            if tokens[i] == "+":
                operand_list.append(n2 + n1)
            elif tokens[i] == "-":
                operand_list.append(n2 - n1)
            elif tokens[i] == "*":
                operand_list.append(n2 * n1)
            else:
                operand_list.append(int(n2 / n1))
    return operand_list[0]
```
* Data structure used: Index mutation adjustments on flat tracking sheets (`list`) for brute force; A single operating Stack (`list`) for optimization.
* Complexity:
  * Brute Force: Time O(N^2) due to expensive array shifting deletions (`pop(index)`) inside loop bounds; Space O(N) duplication buffers.
  * Optimized: Time O(N), since each token is pushed to and popped from the stack at most once; Space O(N) to collect the numeric values.
* Mistakes made: Using the alphanumeric validation helper `.isalnum()` to check if token indices represented integers or operational strings. While this logic initially passed general positive data tests, it immediately triggered code failures on negative integers because the minus hyphen symbol (`-`) returns `False` inside character sets, forcing the engine to mistake numeric values for operational tokens. I resolved this bug by combining a specialized `.isdigit()` fallback alongside a string slicing prefix check (`.startswith('-')`).
* What I learned: `.isalnum()` is unsuitable for token parsing here because negative integers contain -, which is not alphanumeric. When building multi-tier data parsers, constructing explicit prefix filters protects the pipeline against unintended edge-case structural misclassifications.