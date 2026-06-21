# Problem 3: Encode Decode Strings

def encode(strs):
    encoded = []
    for word in strs:
        encoded.append(f"{len(word)}#{word}")
    return "".join(encoded)

def decode(s):
    decode_list = []
    i = 0
    while i < len(s):
        j = i
        while s[j] != "#":
            j += 1
        length = int(s[i:j])
        word = s[j + 1 : j + 1 + length]
        decode_list.append(word)
        i = j + 1 + length
    return decode_list

strs = ["hi", "elephant"]
s = encode(strs)
print(s)
print(decode(s))