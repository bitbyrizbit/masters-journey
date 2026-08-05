class Solution:
    def getSum(self, a, b):
        mask = 0xFFFFFFFF
        mx = 0x7FFFFFFF
        
        while b != 0:
            c = ((a & b) << 1) & mask
            a = (a ^ b) & mask
            b = c
            
        return a if a <= mx else ~(a ^ mask)
