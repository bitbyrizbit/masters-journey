from collections import Counter

class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        # Count the frequency of each task
        counts = Counter(tasks)
        max_freq = max(counts.values())
        
        # Count how many tasks have the maximum frequency
        max_count = sum(1 for count in counts.values() if count == max_freq)
        
        # Calculate the minimum slots required based on the most frequent tasks.
        # We partition the timeline into (max_freq - 1) blocks.
        # Each block is of size (n + 1) to accommodate the cooldown period.
        # Finally, we add the count of tasks that share the maximum frequency.
        min_slots = (max_freq - 1) * (n + 1) + max_count
        
        # The result is the maximum of the calculated slots and the actual number of tasks.
        # If the number of tasks is larger, we can fill the idle slots without expanding the timeline.
        return max(len(tasks), min_slots)

if __name__ == "__main__":
    sol = Solution()
    print(sol.leastInterval(["A","A","A","B","B","B"], 2)) # Output: 8 (A -> B -> idle -> A -> B -> idle -> A -> B)
    print(sol.leastInterval(["A","A","A","B","B","B"], 0)) # Output: 6
    print(sol.leastInterval(["A","A","A","A","A","A","B","C","D","E","F","G"], 2)) # Output: 16
