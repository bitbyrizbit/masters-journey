ops = ["5","-2","4","C","D","9","+","+"]

def baseball_game(ops):
    stack = []
    for s in ops:
        if s == "C" and stack:
            stack.pop()
        elif s == "D" and stack:
            stack.append(stack[-1] * 2)
        elif s == "+" and len(stack) >= 2:
            stack.append(stack[-1] + stack[-2])
        else:
            stack.append(int(s))
    return sum(stack)

print(baseball_game(ops))
