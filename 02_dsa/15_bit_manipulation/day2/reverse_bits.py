class Solution:
    def reverseBits(self, n):
        ans = 0
        for i in range(32):
            b = (n >> i) & 1
            ans |= (b << (31 - i))
        return ans
