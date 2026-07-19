from collections import deque

class Solution:
    def ladder(self, beginWord, endWord, wordList):
        words = set(wordList)
        
        if endWord not in words:
            return 0
        
        queue = deque([(beginWord, 1)])
        visit = {beginWord}
        
        while queue:
            word, length = queue.popleft()
            if word == endWord:
                return length
            for i in range(len(word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    next_word = word[:i] + c + word[i+1:]
                    if next_word in words and next_word not in visit:
                        visit.add(next_word)
                        queue.append((next_word, length + 1))
        return 0

beginWord_input = "hit"
endWord_input = "cog"
wordList_input = ["hot", "dot", "dog", "lot", "log", "cog"]
sol = Solution()
print(sol.ladder(beginWord_input, endWord_input, wordList_input))