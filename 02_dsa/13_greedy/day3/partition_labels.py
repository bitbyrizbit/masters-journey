class Solution:
    def partitionLabels(self, s: str) -> list[int]:
        # Track the last occurrence index of each character
        last_occurrence = {char: idx for idx, char in enumerate(s)}
        
        partitions = []
        start = 0
        end = 0
        
        for idx, char in enumerate(s):
            # Update the end boundary of the current partition
            end = max(end, last_occurrence[char])
            
            # If the current index matches our partition boundary
            if idx == end:
                partitions.append(end - start + 1)
                start = idx + 1
                
        return partitions

if __name__ == "__main__":
    sol = Solution()
    print(sol.partitionLabels("ababcbacadefegdehijhklij")) # Output: [9, 7, 8]
    print(sol.partitionLabels("eccbbbbdec"))               # Output: [10]
