class Solution:
    def find_center(self, edges):
        if edges[0][0] == edges[1][0] or edges[0][0] == edges[1][1]:
            return edges[0][0]
        return edges[0][1]

edges_input = [[1,2],[2,3],[4,2]]
sol = Solution()
print(sol.find_center(edges_input))