def valid_palindrome(s):
    my_str = [char.lower() for char in s if char.isalnum()]
    return my_str == my_str[::-1]

print(valid_palindrome("A man, a plan, a canal: Panama"))

def valid_palindrome_two_pointer(s):
    left = 0
    right = len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
print(valid_palindrome_two_pointer("A man, a plan, a canal: Panama"))
