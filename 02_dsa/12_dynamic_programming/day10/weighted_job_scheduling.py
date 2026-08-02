import bisect

class Solution:
    def jobScheduling(self, startTime: list[int], endTime: list[int], profit: list[int]) -> int:
        # DP + Binary Search (Weighted Interval Scheduling)
        
        n = len(startTime)
        # Combine and sort jobs by their END TIME
        jobs = sorted(zip(startTime, endTime, profit), key=lambda x: x[1])
        
        # Extract sorted end times for binary searching
        end_times = [job[1] for job in jobs]
        
        # dp[i] = max profit taking a subset of the first i jobs
        # dp[0] is initialized to 0 (0 jobs = 0 profit)
        dp = [0] * (n + 1)
        
        for i in range(1, n + 1):
            current_start, current_end, current_profit = jobs[i-1]
            
            # Binary search to find the latest job that finishes BEFORE the current job starts.
            # bisect_right returns the insertion point. If we search for current_start, 
            # it points to the first job that ends strictly AFTER current_start.
            # Thus, the valid non-overlapping job is at index `idx` in our DP array.
            idx = bisect.bisect_right(end_times, current_start)
            
            # Choice 1: Skip current job (inherit max profit from previous job)
            # Choice 2: Take current job (current profit + max profit from the valid non-overlapping job)
            dp[i] = max(dp[i-1], current_profit + dp[idx])
            
        return dp[n]

if __name__ == "__main__":
    sol = Solution()
    print(sol.jobScheduling([1,2,3,3], [3,4,5,6], [50,10,40,70])) # 120 (Job 1 + Job 4)
    print(sol.jobScheduling([1,2,3,4,6], [3,5,10,6,9], [20,20,100,70,60])) # 150
