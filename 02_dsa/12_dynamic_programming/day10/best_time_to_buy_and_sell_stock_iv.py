class Solution:
    def maxProfit(self, k: int, prices: list[int]) -> int:
        # State Machine DP / 3D DP Array
        
        n = len(prices)
        if n == 0 or k == 0:
            return 0
            
        # Optimization: If k is massively large (k >= n/2), we can just execute 
        # infinite transactions (Buy & Sell II approach) to avoid Memory Limit Exceeded.
        if k >= n // 2:
            return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))
            
        # dp[transaction_number][day][holding_status]
        # Instead of a full 3D array, we compress the 'day' dimension to $O(K)$ space
        # by only tracking the 'current' state of each transaction limit.
        
        # Tracks the maximum profit on day i holding NO stock, having completed j transactions
        sell = [0] * (k + 1)
        
        # Tracks the maximum profit on day i HOLDING a stock, having initiated j transactions
        # Initialized to -infinity since it costs money to buy the first stock.
        buy = [float('-inf')] * (k + 1)
        
        for price in prices:
            for j in range(1, k + 1):
                # We can either HOLD the stock we already have (buy[j]), 
                # or we can BUY today using the profit from j-1 completed transactions (sell[j-1] - price).
                buy[j] = max(buy[j], sell[j-1] - price)
                
                # We can either CONTINUE NOT HOLDING (sell[j]),
                # or we can SELL the stock we hold today (buy[j] + price).
                sell[j] = max(sell[j], buy[j] + price)
                
        return sell[k]

if __name__ == "__main__":
    sol = Solution()
    print(sol.maxProfit(2, [2,4,1])) # 2 (Buy at 2, Sell at 4)
    print(sol.maxProfit(2, [3,2,6,5,0,3])) # 7 (Buy at 2, Sell at 6, Buy at 0, Sell at 3)
