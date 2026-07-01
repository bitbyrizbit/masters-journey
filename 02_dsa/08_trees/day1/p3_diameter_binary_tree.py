from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        self.diameter = 0
        def dfs(node):
            if not node:
                return 0
            left = dfs(node.left)
            right = dfs(node.right)
            self.diameter = max(self.diameter, left + right)
            return max(left, right) + 1
        dfs(root)
        return self.diameter

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
root = TreeNode(1)
root.left = TreeNode(2, TreeNode(4), TreeNode(5))
root.right = TreeNode(3)
print("Tree Structure:   ", end="")
print_tree_level_order(root)
diameter = sol.diameterOfBinaryTree(root)
print("Diameter of Tree: ", diameter)