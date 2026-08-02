class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        # Complete Knapsack Counting DP
        
        dp = [0] * (amount + 1)
        dp[0] = 1 # Base case: 1 way to make amount 0 (use no coins)
        
        for coin in coins:
            # Iterate forward (Complete Knapsack: elements can be reused infinitely)
            for current_amount in range(coin, amount + 1):
                dp[current_amount] += dp[current_amount - coin]
                
        return dp[amount]

if __name__ == "__main__":
    sol = Solution()
    print(sol.change(5, [1, 2, 5]))  # 4
    print(sol.change(3, [2]))        # 0
