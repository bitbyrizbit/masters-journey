def calculate(s):
    stack = []
    num = 0
    res = 0
    sign = 1
    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)
        elif char == '+':
            res += sign * num
            num = 0
            sign = 1
        elif char == '-':
            res += sign * num
            num = 0
            sign = -1
        elif char == '(':
            stack.append(res)
            stack.append(sign)
            res = 0
            sign = 1
        elif char == ')':
            res += sign * num
            num = 0
            res *= stack.pop()
            res += stack.pop()
    return res + sign * num

print(calculate("1 + 1"))
print(calculate(" 2-1 + 2 "))
print(calculate("(1+(4+5+2)-3)+(6+8)"))
