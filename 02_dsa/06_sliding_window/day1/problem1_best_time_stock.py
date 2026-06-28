prices = [7,1,5,3,6,4]

def best_time_stock(prices):
    buy = 0 
    sell = 1  
    max_profit = 0
    while sell < len(prices):
        if prices[buy] < prices[sell]:
            current_profit = prices[sell] - prices[buy]
            max_profit = max(max_profit, current_profit)
        else:
            buy = sell
        sell += 1
    return max_profit

print(best_time_stock(prices))
