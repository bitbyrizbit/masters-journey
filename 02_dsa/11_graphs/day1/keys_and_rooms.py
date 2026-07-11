class Solution:
    def visit_rooms(self, rooms):
        visit = set()
        
        def dfs(room):
            visit.add(room)
            for key in rooms[room]:
                if key not in visit:
                    dfs(key)
        dfs(0)
        return len(visit) == len(rooms)

rooms_input = [[1],[2],[3],[]]
sol = Solution()
print(sol.visit_rooms(rooms_input))
