class Solution:
    def reconstructQueue(self, people: list[list[int]]) -> list[list[int]]:
        # Sort people:
        # 1. Descending by height (tallest people first)
        # 2. Ascending by count k (for people of the same height)
        people.sort(key=lambda x: (-x[0], x[1]))
        
        queue = []
        for p in people:
            # Insert the person at index equal to their count k.
            # Since we process tallest people first, all people already in the queue 
            # are taller than or equal in height to the current person. 
            # Thus, inserting the current person at index k guarantees there are 
            # exactly k people in front who are taller or equal.
            queue.insert(p[1], p)
            
        return queue

if __name__ == "__main__":
    sol = Solution()
    print(sol.reconstructQueue([[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]))
    # Output: [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
