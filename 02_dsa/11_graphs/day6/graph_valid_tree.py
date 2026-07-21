class Solution:
    def valid_tree(self, n, edges):
        if len(edges) != n - 1:
            return False
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
                return False
        return True

n_input = 5
edges_input = [[0, 1], [0, 2], [0, 3], [1, 4]]
sol = Solution()
print(sol.valid_tree(n_input, edges_input))