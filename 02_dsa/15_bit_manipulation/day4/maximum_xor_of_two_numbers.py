class TrieNode:
    def __init__(self):
        self.ch = {}

class Solution:
    def findMaximumXOR(self, nums):
        root = TrieNode()
        
        for x in nums:
            cur = root
            for i in range(31, -1, -1):
                b = (x >> i) & 1
                if b not in cur.ch:
                    cur.ch[b] = TrieNode()
                cur = cur.ch[b]
                
        ans = 0
        
        for x in nums:
            cur = root
            val = 0
            
            for i in range(31, -1, -1):
                b = (x >> i) & 1
                nxt = 1 - b
                
                if nxt in cur.ch:
                    val |= (1 << i)
                    cur = cur.ch[nxt]
                else:
                    cur = cur.ch[b]
                    
            ans = max(ans, val)
            
        return ans
