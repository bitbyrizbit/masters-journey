class Solution:
    def count_components(self, n, edges):
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
        
        for u, v in edges:
            res -= union(u, v)
        return res

n_input = 5
edges_input = [[0, 1], [1, 2], [3, 4]]
sol = Solution()
print(sol.count_components(n_input, edges_input))