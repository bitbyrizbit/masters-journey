# functions examples
def power(base, exponent=2):
    return base ** exponent
print(power(3))

def calculate_total(*args, **kwargs):
    total = sum(args)
    if kwargs.get('discount', 0):
        total -= kwargs['discount']
    return total
print(calculate_total(10, 20, 30))
print(calculate_total(10, 20, 30, discount=15))



# lambda examples
my_list = list(filter(lambda x: (x > 10 and x % 3 == 0), range(21)))
print(my_list)



# sorting examples
pairs = [(4, 20), (1, 50), (9, 10)]
pairs.sort(key = lambda x: x[1])
print(pairs)

s = "tree"
sorted_s = sorted(s, key=lambda x: s.count(x), reverse=True)  # O(n^2) because count is O(n) and we call it for each character
print(sorted_s)                                       

s = "tree"
my_dict = {}
for char in s:
    my_dict[char] = my_dict.get(char, 0) + 1
sorted_s = sorted(s, key=lambda x: my_dict[x], reverse=True)  # O(n) to build the dictionary + O(n log n) to sort
print(sorted_s)



# deque examples
from collections import deque
d = deque()
d.append("A")
d.append("B")
d.append("C")
d.popleft()
d.popleft()
print(d)

def moving_average(d, new_val, k):
    d.append(new_val)
    if len(d) > k:
        d.popleft()
    return sum(d) / len(d)

stream_queue = deque()
window_size = 3

print(moving_average(stream_queue, 10, window_size))  # Output: 10.0 (Queue:)
print(moving_average(stream_queue, 20, window_size))  # Output: 15.0 (Queue:)
print(moving_average(stream_queue, 30, window_size))  # Output: 20.0 (Queue:)
print(moving_average(stream_queue, 40, window_size))  # Output: 30.0 (Queue: [20, 30, 40] -> 10 dropped!)



# heapq examples
import heapq
nums = [7, 10, 4, 3, 20, 15]
heapq.heapify(nums)
for i in range(3):
    elem = heapq.heappop(nums)
print(elem)

points = [(0, 2), (4, 4), (1, 1)]
coords = []
for i in points:
    dist = round((i[0]**2 + i[1]**2)**1.5,2)
    coords.append((-dist,i))
heapq.heapify(coords)
heapq.heappop(coords)
print(coords)