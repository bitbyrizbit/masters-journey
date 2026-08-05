class Solution:
    def canJump(self, nums: list[int]) -> bool:
        max_reach = 0
        n = len(nums)
        
        for i in range(n):
            # If the current index is unreachable, we cannot proceed
            if i > max_reach:
                return False
            # Update the furthest index we can reach
            max_reach = max(max_reach, i + nums[i])
            # Early exit: if we can already reach the end, return True
            if max_reach >= n - 1:
                return True
                
        return True

if __name__ == "__main__":
    sol = Solution()
    print(sol.canJump([2,3,1,1,4])) # Output: True
    print(sol.canJump([3,2,1,0,4])) # Output: False
