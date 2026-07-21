class Solution:
    def connected(self, n, connections):
        if len(connections) < n - 1:
            return -1
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
        components = n
        
        for u, v in connections:
            components -= union(u, v)
        return components - 1

n_input = 4
connections_input = [[0, 1], [0, 2], [1, 2]]
sol = Solution()
print(sol.connected(n_input, connections_input))