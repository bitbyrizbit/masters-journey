class Solution:
    def redundant(self, edges):
        parent = list(range(len(edges) + 1))
        rank = [1] * (len(edges) + 1)
        
        def find(n1):
            res = n1
            while res != parent[res]:
                parent[res] = parent[parent[res]]
                res = parent[res]
            return res
        
        def union(n1, n2):
            p1, p2 = find(n1), find(n2)
            if p1 == p2:
                return False
            if rank[p1] > rank[p2]:
                parent[p2] = p1
                rank[p1] += rank[p2]
            else:
                parent[p1] = p2
                rank[p2] += rank[p1]
            return True
        
        for u, v in edges:
            if not union(u, v):
                return [u, v]

edges_input = [[1, 2], [1, 3], [2, 3]]
sol = Solution()
print(sol.redundant(edges_input))