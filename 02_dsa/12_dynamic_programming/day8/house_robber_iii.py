from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        # Tree DP: Postorder Traversal returning multiple states
        # state definition: return (max_if_robbed, max_if_skipped)
        
        def dfs(node: Optional[TreeNode]) -> tuple[int, int]:
            if not node:
                return (0, 0)
                
            # Postorder: fully resolve left and right children first
            left_robbed, left_skipped = dfs(node.left)
            right_robbed, right_skipped = dfs(node.right)
            
            # Transition Logic:
            # If we ROB the current node, we CANNOT rob its direct children
            rob_current = node.val + left_skipped + right_skipped
            
            # If we SKIP the current node, we are FREE to either rob or skip its children (take the max of both)
            skip_current = max(left_robbed, left_skipped) + max(right_robbed, right_skipped)
            
            return (rob_current, skip_current)
            
        return max(dfs(root))

if __name__ == "__main__":
    # Tree: [3, 2, 3, null, 3, null, 1]
    root = TreeNode(3)
    root.left = TreeNode(2, None, TreeNode(3))
    root.right = TreeNode(3, None, TreeNode(1))
    
    sol = Solution()
    print(sol.rob(root)) # 7 (3 + 3 + 1)
