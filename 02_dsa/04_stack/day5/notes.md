## Problem: Decode String

* Brute force: Scanning the string repeatedly from scratch to find the innermost matching bracket pairs `[...]`, expanding the characters manually via replication string builders, and re-stitching the string over multiple passes until no brackets remain.
```python
def decode_string_brute(s):
    # Repeatedly scanning and mutating string slices creates high allocation overhead.
```
* Optimized: Processing the characters in a single pass while utilizing a stack to push the accumulated outer text string and repeat multiplier integer upon hitting `[`, and popping them to dynamically build the nested sequence upon hitting `]`.
```python
def decode_string(s):
    stack = []
    string = ""
    num = 0
    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)
        elif char == '[':
            stack.append((string, num))
            string = ""
            num = 0
        elif char == ']':
            prev_string, num = stack.pop()
            string = prev_string + (string * num)            
        else:
            string += char
    return string
```
* Data structure used: A state-tracking Stack (`list`) capturing nested tuples of `(str, int)` for optimization.
* Complexity:
  * Brute Force: Time $O(n^2)$ due to repeatedly slicing and rewriting the string buffer; Space $O(n)$.
  * Optimized: Time $O(n + m)$ where `n` is the length of the string and `m` is the total length of the decoded output; Space $O(n + m)$ to buffer character snapshots inside the stack.
* Pattern Recognition:
  * Use a stack when:
    - Elements have nested, hierarchical dependencies (like brackets inside brackets).
    - You need to temporarily freeze a current running context (`string`, `num`) and resume it later.
    - Resolving an inner segment requires combining it with the immediate outer context.
* Mistakes made: Initial difficulty was figuring out how to prevent inner decoded layers from accidentally overwriting or erasing the surrounding text block context before the multiplier could be applied. The breakthrough hurdle was tracking the exact ordering of string concatenation from left to right (`prev_string + (string * num)`) and remembering to explicitly reset both `string = ""` and `num = 0` the moment an opening bracket `[` is triggered so that fresh nested frames don't inherit old values.
* What I learned: Strings containing nested multiplication tags are best resolved from the inside out. Stacking the outer text structure alongside its multiplier acts like an elegant bookmarking system, ensuring that nested sequences expand in correct mathematical order without requiring recursion.

---

## Problem: Simplify Path

* Brute force: Navigating the raw directory string character by character with explicit pointer manipulations, maintaining complex sliding index flags to catch empty segments or directory steps manually.
```python
def simplify_path_brute(path):
    # Manual tracking of forward slashes and dot combinations leads to nested, bug-prone loops.
```
* Optimized: Splitting the string cleanly by the `/` delimiter into structural tokens, and iterating through them to pop from a stack on `..` or append valid directory names while skipping empty or `.` steps.
```python
def simplify_path(path):
    tokens = path.split("/")
    stack = []
    for token in tokens:
        if token == "" or token == ".":
            continue
        elif token == "..":
            if stack:
                stack.pop()
        else:
            stack.append(token)
    return "/" + "/".join(stack)
```
* Data structure used: A linear Directory Tracker Stack (`list`) combined with string token splits for optimization.
* Complexity:
  * Brute Force: High code complexity and manual lookbehinds, yet, $O(n)$ time in theory. However, far more error-prone and implementation-heavy due to manual parsing; Space $O(n)$.
  * Optimized: Time $O(n)$ since the split tokens are evaluated in a single sequential sweep; Space $O(n)$ to house the separated paths and stack layout.
* Pattern Recognition:
  * Use a stack when:
    - Direct "go-back" or directory traversal mechanics (like the `..` undo step).
    - Compacting paths or structural tracking arrays where intermediate noise needs to be deleted.
    - String stream filtering based on clean delimiter fields.
* Mistakes made: Initial difficulty was overcoming the instinct to parse the path string character by character, which creates a chaotic maze of tracking variables to handle multiple consecutive slashes `//`. The thought-driven bottleneck was realizing the path should be broken down completely into standalone components using `.split("/")`, and recognizing that the stack must be protected via `if stack:` to prevent underflow errors when excess parent directory commands are supplied at the root level.
* What I learned: Pre-processing an unstructured path string via `.split("/")` strips away matching redundancy and simplifies raw text parsing. It treats directory systems as a clean series of pushing forward or dropping backward, turning a messy string problem into a basic stack-popping loop.

---

## Problem: Basic Calculator

* Brute force: Parsing the mathematical expression string by generating a formal abstract syntax tree (AST) or building complex recursive evaluation systems that continuously slice parentheses boundaries.
```python
def calculate_brute(s):
    # Slicing parenthetical scopes and recursively evaluating equations creates high overhead.
```
* Optimized: Evaluating numbers dynamically using a single pass with sign toggles (`1` for positive, `-1` for negative), caching current tracking states onto a stack whenever `(` is entered, and unpacking the parameters back to resolve calculations upon exiting `)`.
```python
def calculate(s):
    stack = []
    num = 0
    res = 0
    sign = 1
    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)
        elif char == '+':
            res += sign * num
            num = 0
            sign = 1
        elif char == '-':
            res += sign * num
            num = 0
            sign = -1
        elif char == '(':
            stack.append(res)
            stack.append(sign)
            res = 0
            sign = 1
        elif char == ')':
            res += sign * num
            num = 0
            res *= stack.pop()
            res += stack.pop()
    return res + sign * num
```
* Data structure used: An active Evaluation Context Stack (`list`) holding numerical results and operator scalars for optimization.
* Complexity:
  * Brute Force: Varies by implementation - Naive repeated substring slicing can degrade toward $O(n²)$ due to repeated allocations; Space $O(n)$.
  * Optimized: Time $O(n)$ for a single linear sweep across the expression characters; Space $O(n)$ to handle the depth of the nested call brackets.
* Pattern Recognition:
  * Use a stack when:
    - Managing mathematical expressions containing variable evaluation scopes.
    - Distributive properties or multi-tier sign alterations require local variables to reset inside groupings.
    - Postponing operations until inner parameters evaluate to a flat scalar value.
* Mistakes made: The primary cognitive hurdle was figuring out how to handle the distributive property of subtraction when entering parentheses (e.g., `-(a + b)` changes signs to `-a - b`) without spinning up a heavy recursive engine. The logical difficulty was realizing that the entire calculation could be flattened into an ongoing addition sequence (`res += sign * num`), and structuring the stack to snapshot both the base result and active operator multiplier to be unwrapped cleanly from the inside out upon hitting `)`.
* What I learned: Parentheses act like local scope blocks in a computer script. By pushing the global values (`res` and `sign`) onto a stack whenever a nested block opens, you can cleanly wipe the operational registers to calculate the localized inner sub-problem independently, before stitching them together seamlessly at the close mark.