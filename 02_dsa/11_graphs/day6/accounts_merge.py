class Solution:
    def accounts_merge(self, accounts):
        parent = list(range(len(accounts)))
        rank = [1] * len(accounts)
        
        def find(n1):
            res = n1
            while res != parent[res]:
                parent[res] = parent[parent[res]]
                res = parent[res]
            return res
        
        def union(n1, n2):
            p1, p2 = find(n1), find(n2)
            if p1 == p2:
                return
            if rank[p1] > rank[p2]:
                parent[p2] = p1
                rank[p1] += rank[p2]
            else:
                parent[p1] = p2
                rank[p2] += rank[p1]
        email_to_acc = {}
        
        for i, acc in enumerate(accounts):
            for email in acc[1:]:
                if email in email_to_acc:
                    union(i, email_to_acc[email])
                else:
                    email_to_acc[email] = i
        res_dict = {}
        
        for email, acc_idx in email_to_acc.items():
            leader = find(acc_idx)
            if leader not in res_dict:
                res_dict[leader] = []
            res_dict[leader].append(email)
        return [[accounts[idx][0]] + sorted(emails) for idx, emails in res_dict.items()]

accounts_input = [["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["John", "johnsmith@mail.com", "john00@mail.com"], ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]
sol = Solution()
print(sol.accounts_merge(accounts_input))