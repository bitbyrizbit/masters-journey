from collections import deque

class Solution:
    def order(self, num_courses, prerequisites):
        adj = {i: [] for i in range(num_courses)}
        indegree = [0] * num_courses
        
        for dest, src in prerequisites:
            adj[src].append(dest)
            indegree[dest] += 1
        queue = deque([i for i in range(num_courses) if indegree[i] == 0])
        order = []
        
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in adj[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
        return order if len(order) == num_courses else []

num_courses = 4
prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
sol = Solution()
print(sol.order(num_courses, prerequisites))