from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # Tree DP: Tracking global maximum while returning a strict linear path
        self.global_max = float('-inf')
        
        def dfs(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
                
            # Postorder: solve children first.
            # If a child's max path is negative, we drop it entirely (max with 0)
            left_max = max(dfs(node.left), 0)
            right_max = max(dfs(node.right), 0)
            
            # State Action 1: Calculate the arch (left + node + right) and update global max
            current_arch = left_max + right_max + node.val
            self.global_max = max(self.global_max, current_arch)
            
            # State Action 2: Return the maximum single linear path ending at this node
            # We CANNOT return an arch to the parent, because a path cannot fork.
            return node.val + max(left_max, right_max)
            
        dfs(root)
        return int(self.global_max)

if __name__ == "__main__":
    # Tree: [-10, 9, 20, null, null, 15, 7]
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20, TreeNode(15), TreeNode(7))
    
    sol = Solution()
    print(sol.maxPathSum(root)) # 42 (15 + 20 + 7)
