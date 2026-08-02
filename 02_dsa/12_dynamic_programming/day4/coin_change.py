class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        # Complete Knapsack Minimum DP
        
        # Initialize DP array with an impossibly high value (infinity proxy)
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0 # Base case: 0 coins needed to make amount 0
        
        for coin in coins:
            # Iterate forward (Complete Knapsack: elements can be reused infinitely)
            for current_amount in range(coin, amount + 1):
                dp[current_amount] = min(dp[current_amount], 1 + dp[current_amount - coin])
                
        return int(dp[amount]) if dp[amount] != float('inf') else -1

if __name__ == "__main__":
    sol = Solution()
    print(sol.coinChange([1, 2, 5], 11))  # 3 (5 + 5 + 1)
    print(sol.coinChange([2], 3))         # -1
