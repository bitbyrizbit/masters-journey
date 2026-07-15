class Solution:
    def canVisitAllRooms(self, rooms: list[list[int]]) -> bool:
        visit = set()
        def dfs(room):
            visit.add(room)
            for key in rooms[room]:
                if key not in visit:
                    dfs(key)
        dfs(0)
        return len(visit) == len(rooms)

rooms_input = [[1], [2], [3], []]
sol = Solution()
print(sol.canVisitAllRooms(rooms_input))
