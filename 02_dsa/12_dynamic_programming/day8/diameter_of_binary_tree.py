from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        # Tree DP: State returns the depth, but modifies a global max diameter
        self.max_diameter = 0
        
        def dfs(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
                
            # Postorder: solve children first to get their depths
            left_depth = dfs(node.left)
            right_depth = dfs(node.right)
            
            # The diameter passing through THIS node is the sum of left and right depths
            self.max_diameter = max(self.max_diameter, left_depth + right_depth)
            
            # The node returns its own depth to its parent (1 + max of children)
            return 1 + max(left_depth, right_depth)
            
        dfs(root)
        return self.max_diameter

if __name__ == "__main__":
    # Tree: [1, 2, 3, 4, 5]
    root = TreeNode(1)
    root.left = TreeNode(2, TreeNode(4), TreeNode(5))
    root.right = TreeNode(3)
    
    sol = Solution()
    print(sol.diameterOfBinaryTree(root)) # 3 (Path: 4->2->1->3 or 5->2->1->3)
