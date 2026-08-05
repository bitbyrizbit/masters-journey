class Solution:
    def jump(self, nums: list[int]) -> int:
        n = len(nums)
        if n <= 1:
            return 0
            
        jumps = 0
        curr_end = 0
        max_reach = 0
        
        # We loop up to n - 2 because if we reach the last index, 
        # we do not need to make another jump.
        for i in range(n - 1):
            max_reach = max(max_reach, i + nums[i])
            
            # If we have reached the end of the current jump's range
            if i == curr_end:
                jumps += 1
                curr_end = max_reach
                # Early exit: if we can already reach the last index
                if curr_end >= n - 1:
                    break
                    
        return jumps

if __name__ == "__main__":
    sol = Solution()
    print(sol.jump([2,3,1,1,4])) # Output: 2
    print(sol.jump([2,3,0,1,4])) # Output: 2
