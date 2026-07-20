from collections import deque

class Solution:
    def finish(self, num_courses, prerequisites):
        adj = {i: [] for i in range(num_courses)}
        indegree = [0] * num_courses
        
        for dest, src in prerequisites:
            adj[src].append(dest)
            indegree[dest] += 1
        queue = deque([i for i in range(num_courses) if indegree[i] == 0])
        visited_count = 0
        
        while queue:
            node = queue.popleft()
            visited_count += 1
            for neighbor in adj[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
        return visited_count == num_courses

num_courses = 2
prerequisites_input = [[1, 0]]
sol = Solution()
print(sol.finish(num_courses, prerequisites_input))