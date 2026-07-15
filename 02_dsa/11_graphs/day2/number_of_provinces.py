class Solution:
    def findCircleNum(self, isConnected: list[list[int]]) -> int:
        n = len(isConnected)
        visit = set()
        provinces = 0
        def dfs(node):
            for neighbor in range(n):
                if isConnected[node][neighbor] == 1 and neighbor not in visit:
                    visit.add(neighbor)
                    dfs(neighbor)
        for i in range(n):
            if i not in visit:
                provinces += 1
                visit.add(i)
                dfs(i)
        return provinces

isConnected_input = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
sol = Solution()
print(sol.findCircleNum(isConnected_input))
