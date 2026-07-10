class Solution:
    def remove_invalid_parentheses(self, s):
        def is_valid(string):
            count = 0
            for c in string:
                if c == "(":
                    count += 1
                elif c == ")":
                    count -= 1
                    if count < 0:
                        return False
            return count == 0
        level = {s}
        while True:
            valid = list(filter(is_valid, level))
            if valid:
                return valid
            next_level = set()
            for string in level:
                for i in range(len(string)):
                    if string[i] in "()":
                        next_level.add(string[:i] + string[i+1:])
            if not next_level:
                return [""]
            level = next_level

s_input = "()())()"
sol = Solution()
print(sol.remove_invalid_parentheses(s_input))