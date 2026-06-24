import itertools

def generate_valid_parentheses(n):
    choice = ["(", ")"]
    raw_combinations = itertools.product(choice, repeat=2 * n)
    valid_list = []
    for s in raw_combinations:
        string = "".join(s)
        balance = 0
        is_valid = True
        for s in string:
            if s == "(":
                balance += 1
            elif s == ")":
                balance -= 1
            
            if balance < 0:
                is_valid = False
                break                 
        if is_valid and balance == 0:
            valid_list.append(string)
    return valid_list

n = 2
print(generate_valid_parentheses(n))

def generate_parentheses_optimal(n):
    result = []
    def backtrack(current_string, open_count, close_count):
        if len(current_string) == 2 * n:
            result.append(current_string)
            return
        if open_count < n:
            backtrack(current_string + "(", open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current_string + ")", open_count, close_count + 1)
    backtrack("", 0, 0)
    return result

n = 3
print(generate_parentheses_optimal(n))