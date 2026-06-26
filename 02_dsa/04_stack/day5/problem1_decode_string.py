def decode_string(s):
    stack = []
    string = ""
    num = 0
    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)
        elif char == '[':
            stack.append((string, num))
            string = ""
            num = 0
        elif char == ']':
            prev_string, num = stack.pop()
            string = prev_string + (string * num)            
        else:
            string += char
    return string

s = "3[a2[c]]"
print(decode_string(s))