class Solution:
    def circle_num(self, isConnected):
        n = len(isConnected)
        parent = list(range(n))
        rank = [1] * n
        
        def find(n1):
            res = n1
            while res != parent[res]:
                parent[res] = parent[parent[res]]
                res = parent[res]
            return res
        
        def union(n1, n2):
            p1, p2 = find(n1), find(n2)
            if p1 == p2:
                return 0
            if rank[p1] > rank[p2]:
                parent[p2] = p1
                rank[p1] += rank[p2]
            else:
                parent[p1] = p2
                rank[p2] += rank[p1]
            return 1
        res = n
        
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j] == 1:
                    res -= union(i, j)
        return res

isConnected_input = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
sol = Solution()
print(sol.circle_num(isConnected_input))