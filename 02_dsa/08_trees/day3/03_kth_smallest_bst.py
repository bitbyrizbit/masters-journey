class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:
    def kthSmallest(self, root, k):
        self.k = k
        self.result = None
        def inorder(node):
            if not node or self.result is not None:
                return
            inorder(node.left)
            self.k -= 1
            if self.k == 0:
                self.result = node.val
                return
            inorder(node.right)            
        inorder(root)
        return self.result

root3 = TreeNode(3)
root3.left = TreeNode(1)
root3.right = TreeNode(4)
root3.left.right = TreeNode(2)

sol = Solution()
print(sol.kthSmallest(root3, k=1))
print(sol.kthSmallest(root3, k=3))  