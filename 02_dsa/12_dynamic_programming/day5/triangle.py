class Solution:
    def minimumTotal(self, triangle: list[list[int]]) -> int:
        # Variable-width Grid DP
        # Optimized approach: Bottom-Up DP using a 1D array
        # This completely eliminates bounds checking for edges!
        
        # Start with the bottom row of the triangle
        n = len(triangle)
        dp = triangle[-1][:]
        
        # Iterate upwards from the second-to-last row to the top
        for row in range(n - 2, -1, -1):
            for i in range(len(triangle[row])):
                # For each element, add the minimum of the two possible children from the row below
                dp[i] = triangle[row][i] + min(dp[i], dp[i+1])
                
        # The top element will accumulate the minimum path sum
        return dp[0]

if __name__ == "__main__":
    sol = Solution()
    print(sol.minimumTotal([[2],[3,4],[6,5,7],[4,1,8,3]]))  # 11 (2->3->5->1)
    print(sol.minimumTotal([[-10]]))                        # -10
