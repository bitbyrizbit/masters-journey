def asteroid_collision(asteroids):
    stack = []
    for ast in asteroids:
        while stack and ast < 0 and stack[-1] > 0:
            diff = ast + stack[-1]
            if diff < 0:
                stack.pop()    
            elif diff > 0:
                ast = 0
                break
            else:
                stack.pop()
                ast = 0
                break
        if ast != 0:
            stack.append(ast)
    return stack

asteroids = [10,2,-5]
print(asteroid_collision(asteroids))