class Solution:
    def rangeBitwiseAnd(self, left, right):
        c = 0
        while left < right:
            left >>= 1
            right >>= 1
            c += 1
        return left << c
