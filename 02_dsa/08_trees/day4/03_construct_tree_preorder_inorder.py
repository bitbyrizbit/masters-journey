from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:
    def buildTree(self, preorder, inorder):
        inorder_map = {val: idx for idx, val in enumerate(inorder)}
        preorder_idx = 0
        def helper(left_inorder_idx, right_inorder_idx):
            nonlocal preorder_idx
            if left_inorder_idx > right_inorder_idx:
                return None
            root_val = preorder[preorder_idx]
            root = TreeNode(root_val)
            preorder_idx += 1
            mid_idx = inorder_map[root_val]
            root.left = helper(left_inorder_idx, mid_idx - 1)
            root.right = helper(mid_idx + 1, right_inorder_idx)
            return root            
        return helper(0, len(inorder) - 1)

preorder = [3, 9, 20, 15, 7]
inorder = [9, 3, 15, 20, 7]

sol = Solution()
new_root = sol.buildTree(preorder, inorder)

print(f"Root: {new_root.val}")
print(f"Left Child: {new_root.left.val}")
print(f"Right Child: {new_root.right.val}")
