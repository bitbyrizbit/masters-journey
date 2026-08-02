from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        # Tree DP: Preorder state passing (Top-Down state accumulation)
        # We must pass the current length and the expected direction down to the children.
        
        self.max_zigzag = 0
        
        def dfs(node: Optional[TreeNode], is_left: bool, length: int):
            if not node:
                return
                
            self.max_zigzag = max(self.max_zigzag, length)
            
            if is_left:
                # If we came from the left, a valid zigzag MUST go right to extend the length
                dfs(node.right, False, length + 1)
                # If we go left anyway, the zigzag breaks and restarts from 1
                dfs(node.left, True, 1)
            else:
                # If we came from the right, a valid zigzag MUST go left to extend the length
                dfs(node.left, True, length + 1)
                # If we go right anyway, the zigzag breaks and restarts from 1
                dfs(node.right, False, 1)
                
        # Kick off DFS in both directions from the root
        dfs(root.left, True, 1)
        dfs(root.right, False, 1)
        
        return self.max_zigzag

if __name__ == "__main__":
    # Constructing a ZigZag tree
    root = TreeNode(1)
    root.right = TreeNode(1)
    root.right.left = TreeNode(1)
    root.right.right = TreeNode(1)
    root.right.right.left = TreeNode(1)
    root.right.right.right = TreeNode(1)
    root.right.right.left.right = TreeNode(1)
    
    sol = Solution()
    print(sol.longestZigZag(root)) # 3
