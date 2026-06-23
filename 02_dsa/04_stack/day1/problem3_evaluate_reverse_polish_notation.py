tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]

def eval_postfix(tokens):
    operand_list = []
    for i in range(len(tokens)):
        if tokens[i].isdigit() or (tokens[i].startswith('-') and tokens[i][1:].isdigit()):
            operand_list.append(tokens[i])
        elif not tokens[i].isalnum():
            n1 = int(operand_list.pop())
            n2 = int(operand_list.pop())
            if tokens[i] == "+":
                operand_list.append(n2 + n1)
            elif tokens[i] == "-":
                operand_list.append(n2 - n1)
            elif tokens[i] == "*":
                operand_list.append(n2 * n1)
            else:
                operand_list.append(int(n2 / n1))
    return operand_list[0]

print(eval_postfix(tokens))