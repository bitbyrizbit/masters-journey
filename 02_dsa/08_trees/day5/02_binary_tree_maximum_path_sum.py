class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        max_sum = float('-inf')
        def gain_dfs(node):
            nonlocal max_sum
            if not node:
                return 0
            left_gain = max(gain_dfs(node.left), 0)
            right_gain = max(gain_dfs(node.right), 0)
            max_sum = max(max_sum, node.val + left_gain + right_gain)
            return node.val + max(left_gain, right_gain)
        gain_dfs(root)
        return max_sum


root = TreeNode(-10)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)
sol = Solution()
print(sol.maxPathSum(root))
