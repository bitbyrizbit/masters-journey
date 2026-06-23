def valid_parentheses(s):
    stack = []
    pairs = ["()", "[]", "{}"]
    for i in s:
        if i == " ":
            continue
        if i in ("(", "[", "{"):
            stack.append(i)
        elif i in (")", "]", "}"):
            if not stack:
                return False
            parentheses = stack.pop() 
            parentheses += i
            if parentheses not in pairs:
                return False 
        else:
            return False
    return len(stack) == 0  

print(valid_parentheses("()"))     
print(valid_parentheses("[]"))     
print(valid_parentheses("(]"))     
print(valid_parentheses("([{])"))  
print(valid_parentheses("(())"))   
print(valid_parentheses("{ }]"))   
print(valid_parentheses("[{ }]"))  
