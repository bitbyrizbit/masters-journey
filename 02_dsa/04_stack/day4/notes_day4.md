## Problem: Baseball Game

* Brute force: No meaningful brute-force alternative exists here without simulating history inefficiently; stack is the natural solution.
* Optimized: Processing operations sequentially using a stack structure to dynamically pop or append calculated metrics based on character symbols, then returning the sum of the final elements.
```python
def baseball_game(ops):
    stack = []
    for s in ops:
        if s == "C" and stack:
            stack.pop()
        elif s == "D" and stack:
            stack.append(stack[-1] * 2)
        elif s == "+" and len(stack) >= 2:
            stack.append(stack[-1] + stack[-2])
        else:
            stack.append(int(s))
    return sum(stack)
```
* Data structure used: Python List (`list`) serving as a sequential score-tracking stack.
* Complexity:
  * Time $O(n)$ for a single-pass processing loop; Space $O(n)$ to maintain stack allocations.
* Mistakes made: Initially adding defensive checks like `and stack` to avoid stack underflow. These are useful in general-purpose code, but LeetCode guarantees valid operations, so they are not strictly required. Similarly, evaluating the `+` operation without ensuring at least two previous scores `(len(stack) >= 2)` could cause an `IndexError` in unconstrained inputs. Under LeetCode’s valid-input guarantees, however, this safety check is optional.
* What I learned: Applying explicit length validations ahead of historical index reads protects stack pointers against underflow crashes. This problem is a perfect example of when a stack models “undo/history” operations naturally. Commands like `C`, `D`, and `+` all depend only on the most recent valid scores, making stack access ideal.

---

## Problem: Remove All Adjacent Duplicates In String

* Brute force: Scanning the string repeatedly inside a loop to look for matching pairs next to each other, using string concatenation to delete them, and restarting the scan until no adjacent duplicates remain.
```python
def remove_adjacent_duplicates_brute(s):
    old_len = -1
    while len(s) != old_len:
        old_len = len(s)
        for i in range(len(s) - 1):
            if s[i] == s[i + 1]:
                s = s[:i] + s[i + 2:]
                break
    return s
```
* Optimized: Traversing the string in a single linear pass using a stack to buffer characters, checking if the current character matches the top of the stack, and popping it off immediately if a duplication event occurs.
```python
def remove_adjacent_duplicates(s):
    stack = []
    for char in s:
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)
    return "".join(stack)
```
* Data structure used: String slicing copy buffers for brute force; A character validation Stack (`list`) for optimization.
* Complexity:
  * Brute Force: Time $O(n^2)$ due to rescanning the mutating string structure over and over; Space $O(n)$ to build slice copies.
  * Optimized: Time $O(n)$ because every character is appended to the stack once and removed at most once; Space $O(n)$ to hold the clean output characters.
* Mistakes made: None. Independently mapped out the optimal data routing step on the very first try.
* What I learned: Instead of performing heavy destructive modifications directly on a string buffer, using a stack turns a multi-pass deletion routine into a quick, single-pass inspection step. The top element of the stack always holds the immediate neighbor for the next character, completely bypassing index calculations.

---

## Problem: Asteroid Collision

* Brute force: Simulating independent movements across a grid using multi-pointer scans, shifting coordinates, and deleting collided array elements step by step.
```python
def asteroid_collision_brute(asteroids):
    # Simulating continuous movement loops leads to complex index shifts and slow allocations.
```
* Optimized: Processing elements with a stack and using a nested `while` loop to trigger dynamic crushing matches exclusively when a left-moving negative asteroid collides with a right-moving positive asteroid.
```python
def asteroid_collision(asteroids):
    stack = []
    for ast in asteroids:
        while stack and ast < 0 and stack[-1] > 0:
            diff = ast + stack[-1]
            if diff < 0:
                stack.pop()    
            elif diff > 0:
                ast = 0
                break
            else:
                stack.pop()
                ast = 0
                break
        if ast != 0:
            stack.append(ast)
    return stack
```
* Data structure used: An active collision-resolution tracking Stack (`list`) for optimization.
* Complexity:
  * Brute Force: Time $O(n^2)$ due to simulating constant state recalculations; Space $O(n)$.
  * Optimized: Time $O(n)$ because each asteroid is pushed or popped from the stack at most once; Space $O(n)$ to store the surviving elements.
* Mistakes made: Initial difficulty was understanding why collisions only happen when a positive asteroid is on stack top and current asteroid is negative. Same-direction asteroids or left-moving followed by right-moving asteroids never collide.
* What I learned: Collisions only occur when a right-moving positive element stands to the left of a left-moving negative element (`ast < 0 and stack[-1] > 0`). By capturing this condition inside a rolling `while` structure, the stack resolves multiple cascading collisions automatically. Setting `ast = 0` acts as a destruction marker, allowing the algorithm to skip appending the current asteroid after collision resolution. The while loop is necessary instead of a single if because one incoming asteroid may destroy multiple smaller positive asteroids already present in the stack before finally stopping or surviving.