from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        return max(left_depth, right_depth) + 1

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

sol = Solution()
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20, TreeNode(15), TreeNode(7))
print("Tree Structure: ", end="")
print_tree_level_order(root)
depth = sol.maxDepth(root)
print("Maximum Depth:  ", depth)
