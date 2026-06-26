def simplify_path(path):
    tokens = path.split("/")
    stack = []
    for token in tokens:
        if token == "" or token == ".":
            continue
        elif token == "..":
            if stack:
                stack.pop()
        else:
            stack.append(token)
    return "/" + "/".join(stack)

print(simplify_path("/a/b/c"))
print(simplify_path("/home//foe"))
print(simplify_path("/../"))