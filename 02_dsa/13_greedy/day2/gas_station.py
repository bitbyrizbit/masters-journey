class Solution:
    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        # If total gas is less than total cost, completing the circuit is mathematically impossible
        if sum(gas) < sum(cost):
            return -1
            
        total_surplus = 0
        curr_surplus = 0
        start_station = 0
        
        for i in range(len(gas)):
            diff = gas[i] - cost[i]
            total_surplus += diff
            curr_surplus += diff
            
            # If the current surplus dips below 0, we cannot start from any station 
            # up to index i. We must reset and try starting from index i + 1.
            if curr_surplus < 0:
                curr_surplus = 0
                start_station = i + 1
                
        return start_station

if __name__ == "__main__":
    sol = Solution()
    print(sol.canCompleteCircuit([1,2,3,4,5], [3,4,5,1,2])) # Output: 3
    print(sol.canCompleteCircuit([2,3,4], [3,4,3]))         # Output: -1
