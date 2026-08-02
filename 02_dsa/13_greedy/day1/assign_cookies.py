class Solution:
    def findContentChildren(self, g: list[int], s: list[int]) -> int:
        # Sort both children greedily by greed factor and cookies by size
        g.sort()
        s.sort()
        
        child_ptr = 0
        cookie_ptr = 0
        
        while child_ptr < len(g) and cookie_ptr < len(s):
            # If the current cookie can satisfy the current child
            if s[cookie_ptr] >= g[child_ptr]:
                # Child is satisfied, move to the next child
                child_ptr += 1
            # Move to the next cookie (whether it was used or too small to satisfy the current child)
            cookie_ptr += 1
            
        return child_ptr

if __name__ == "__main__":
    sol = Solution()
    print(sol.findContentChildren([1,2,3], [1,1]))  # Output: 1
    print(sol.findContentChildren([1,2], [1,2,3]))  # Output: 2
