from collections import deque

class MinStack:
    def __init__(self):
        self.min_stack = deque()

    def push(self, val: int) -> None:
        self.min_stack.append(val)

    def pop(self) -> None:
        self.min_stack.pop()

    def top(self) -> int:
        return self.min_stack[-1] if self.min_stack else None

    def getMin(self) -> int:
        return min(self.min_stack) if self.min_stack else None

minStack = MinStack()
minStack.push(-2)
minStack.push(0)
minStack.push(-3)

print(minStack.getMin()) 
minStack.pop()
print(minStack.top())     
print(minStack.getMin())  
