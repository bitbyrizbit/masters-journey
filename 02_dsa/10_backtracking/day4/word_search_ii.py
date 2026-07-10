class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def add_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node.node = node.children[char]
        node.is_word = True

class Solution:
    def find(self, board, words):
        root = TrieNode()
        for w in words:
            node = root
            for c in w:
                if c not in node.children:
                    node.children[c] = TrieNode()
                node = node.children[c]
            node.is_word = True
        ROWS, COLS = len(board), len(board[0])
        res, visit = set(), set()
        def dfs(r, c, node, word):
            if (r < 0 or c < 0 or r >= ROWS or c >= COLS or 
                board[r][c] not in node.children or (r, c) in visit):
                return
            visit.add((r, c))
            node = node.children[board[r][c]]
            word += board[r][c]
            if node.is_word:
                res.add(word)
            dfs(r + 1, c, node, word)
            dfs(r - 1, c, node, word)
            dfs(r, c + 1, node, word)
            dfs(r, c - 1, node, word)
            visit.remove((r, c))
        for r in range(ROWS):
            for c in range(COLS):
                dfs(r, c, root, "")
        return list(res)

board_input = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
words_input = ["oath","pea","eat","rain"]
sol = Solution()
print(sol.find(board_input, words_input))