class Solution:
    def amountPainted(self, paint):
        if not paint:
            return []
            
        mx = max(e for _, e in paint)
        nxt = [0] * (mx + 1)
        ans = []
        
        for s, e in paint:
            work = 0
            i = s
            while i < e:
                if nxt[i] == 0:
                    work += 1
                    nxt[i] = i + 1
                    i += 1
                else:
                    tmp = nxt[i]
                    nxt[i] = max(nxt[i], e)
                    i = tmp
            ans.append(work)
            
        return ans
