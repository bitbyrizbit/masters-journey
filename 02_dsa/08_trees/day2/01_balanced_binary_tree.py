from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def balanced_binary(node):
    if node is None:
        return True, 0

    left_balanced, left_height = balanced_binary(node.left)
    right_balanced, right_height = balanced_binary(node.right)

    current_balanced = left_balanced and right_balanced and abs(left_height - right_height) <= 1
    current_height = max(left_height, right_height) + 1

    return current_balanced, current_height

def print_tree_level_order(root):
    if not root:
        print("Empty Tree")
        return
    res = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node:
            res.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            res.append(None)
    while res and res[-1] is None:
        res.pop()
    print(res)


root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20, TreeNode(15), TreeNode(7))

print("Tree Structure: ", end="")
print_tree_level_order(root)

is_balanced, height = balanced_binary(root)
print("Is Balanced:   ", is_balanced)
print("Tree Height:   ", height)
