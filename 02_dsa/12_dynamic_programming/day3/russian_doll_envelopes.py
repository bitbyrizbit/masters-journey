import bisect

class Solution:
    def maxEnvelopes(self, envelopes: list[list[int]]) -> int:
        if not envelopes:
            return 0
            
        # Sort by width ascending, then height descending
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        
        # Extract heights
        heights = [env[1] for env in envelopes]
        
        # Run O(N log N) LIS on heights
        tails = []
        for h in heights:
            idx = bisect.bisect_left(tails, h)
            if idx == len(tails):
                tails.append(h)
            else:
                tails[idx] = h
                
        return len(tails)

envelopes_input = [[5, 4], [6, 4], [6, 7], [2, 3]]
sol = Solution()
print(sol.maxEnvelopes(envelopes_input))  # Output: 3 (Envelopes are [2, 3] => [5, 4] => [6, 7])
