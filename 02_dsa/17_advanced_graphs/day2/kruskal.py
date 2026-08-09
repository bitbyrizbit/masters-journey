class Solution:
    def minCostConnectPoints(self, points):
        n = len(points)
        parent = list(range(n))
        
        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]
            
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_j] = root_i
                return True
            return False
            
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                d = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                edges.append((d, i, j))
                
        edges.sort()
        ans = 0
        cnt = 0
        for d, u, v in edges:
            if union(u, v):
                ans += d
                cnt += 1
                if cnt == n - 1:
                    break
        return ans
