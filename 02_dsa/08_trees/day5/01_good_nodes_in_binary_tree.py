class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:
    def goodNodes(self, root):
        def dfs(node, max_so_far):
            if not node:
                return 0
            is_good = 1 if node.val >= max_so_far else 0
            max_so_far = max(max_so_far, node.val)
            return is_good + dfs(node.left, max_so_far) + dfs(node.right, max_so_far)
        return dfs(root, root.val) if root else 0


root = TreeNode(3)
root.left = TreeNode(1)
root.right = TreeNode(4)
root.left.left = TreeNode(3)
root.right.left = TreeNode(1)
root.right.right = TreeNode(5)
sol = Solution()
print(sol.goodNodes(root))
