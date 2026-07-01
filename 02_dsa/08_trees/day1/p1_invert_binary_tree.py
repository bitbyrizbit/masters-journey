from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        if not root:
            return root
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root

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
root = TreeNode(4)
root.left = TreeNode(2, TreeNode(1), TreeNode(3))
root.right = TreeNode(7, TreeNode(6), TreeNode(9))
print("Initial Tree:  ", end="")
print_tree_level_order(root)
inverted_root = sol.invertTree(root)
print("Inverted Tree: ", end="")
print_tree_level_order(inverted_root)