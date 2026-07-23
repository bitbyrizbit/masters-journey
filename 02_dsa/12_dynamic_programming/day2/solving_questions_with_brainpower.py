class Solution:
    def most_points(self, questions: list[list[int]]) -> int:
        n = len(questions)
        dp = [0] * (n + 1)
        
        for i in range(n - 1, -1, -1):
            points, brainpower = questions[i]
            next_question = i + brainpower + 1
            
            solve = points + (dp[next_question] if next_question < n else 0)
            
            skip = dp[i + 1]
            
            dp[i] = max(solve, skip)
            
        return dp[0]

questions_input = [[3, 2], [4, 3], [4, 4], [2, 5]]
sol = Solution()
print(sol.most_points(questions_input)) 
