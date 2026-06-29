def fruits_in_basket(fruits):
    if not fruits:
        return 0
    char_map = {}
    left = 0
    max_length = 0
    for right in range(len(fruits)):
        char_map[fruits[right]] = char_map.get(fruits[right], 0) + 1
        while len(char_map) > 2:
            char_map[fruits[left]] -= 1
            if char_map[fruits[left]] == 0:
                del char_map[fruits[left]]
            left += 1
        max_length = max(max_length, right - left + 1)
    return max_length

fruits = [0,1,2,2]
print(fruits_in_basket(fruits))
