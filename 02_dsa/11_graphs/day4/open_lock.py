from collections import deque

class Solution:
    def open_lock(self, deadends, target):
        dead = set(deadends)
        if "0000" in dead:
            return -1
        
        queue = deque([("0000", 0)])
        visit = {"0000"}
        
        while queue:
            lock, turns = queue.popleft()
            if lock == target:
                return turns
            for i in range(4):
                digit = int(lock[i])
                for move in [-1, 1]:
                    new_digit = (digit + move) % 10
                    new_lock = lock[:i] + str(new_digit) + lock[i+1:]
                    if new_lock not in dead and new_lock not in visit:
                        visit.add(new_lock)
                        queue.append((new_lock, turns + 1))
        return -1

deadends_input = ["0201", "0101", "0102", "1212", "2002"]
target_input = "0202"
sol = Solution()
print(sol.open_lock(deadends_input, target_input))