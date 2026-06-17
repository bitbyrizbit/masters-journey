# list comprehension examples
numbers = [1, 2, 3, 4, 5]
squared_numbers = [num**2 for num in numbers]
print(squared_numbers)

even_odd = [10, 15, 20, 25, 30, 35]
even_numbers = [even for even in even_odd if even % 2 == 0]
print(even_numbers)

fruits = ["apple", "banana", "cherry"]
uppercase_fruits = [fruit.upper() for fruit in fruits]
print(uppercase_fruits)

names = ["Joe", "Amelia", "Bo", "Charlie"]
name_count = [len(name) for name in names]
print(name_count)

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed_matrix = [list(row) for row in zip(*matrix)]
print(transposed_matrix)

data = [[1, "apple", 2], ["banana", 3], [4, 5, "cherry"]]
flattened_data = [x for row in data for x in row if isinstance(x,int)]
print(flattened_data)



# lambda examples
num = 7 
double = lambda x: x * 2 
result = double(num)
print(result)

numbers = [1, 2, 3, 4, 5, 6]
print(list(filter(lambda x: x % 2 != 0, numbers)))

names = ["Alice", "Bob", "Charlie"]
print(list(map(lambda x: x[0], names)))



# map examples
prices = [5, 12, 27, 40]
print(list(map(lambda x: x + 10, prices)))

string_nums = ["1", "5", "9", "22"]
print(list(map(int, string_nums)))

users = ["Sam", "Luna", "Alex"]
print(list(map(lambda x: "Hello, " + x, users)))

numbers = [10, 15, 22, 33]
print(list(map(lambda x: x % 3, numbers)))



# zip examples
names = ["Alice", "Bob", "Charlie"]
ids = [101, 102, 103]
print(list(zip(names, ids)))

keys = ["brand", "model", "year"]
values = ["Ford", "Mustang", 1964]
print(dict(zip(keys, values)))

items = ["apple", "banana", "cherry", "date"]
prices = [1.5, 0.8, 2.5]
print(list(zip(items, prices)))



# enumerate examples
tasks = ["Write code", "Test code", "Deploy code"]
print(list(enumerate(tasks, start=0)))

numbers = [10, 20, 30, 40, 50]
indices = list(enumerate(numbers, start=1))
print([value for index, value in indices if index % 2 == 0])



# Counter examples
from collections import Counter
word = "banana"
print(Counter(word))

votes = ["apple", "banana", "apple", "cherry", "apple", "banana"]
print(Counter(votes).most_common(1))

sentence = "apple banana apple cherry"
print(Counter(sentence.split()))

branch_a = Counter(apples=4, bananas=2)
branch_b = Counter(apples=1, cherries=5)
print(Counter(branch_a) + Counter(branch_b))



# defaultdict examples
from collections import defaultdict
items = ["apple", "banana", "apple", "cherry", "apple"]
default_dict = defaultdict(int)
for item in items:
    default_dict[item] += 1
print(default_dict)

numbers = [2, 4, 6]
default_dict = defaultdict(list)
for num in numbers:
    default_dict["even" if num % 2 == 0 else "odd"].append(num)
print(default_dict)



# deque examples
from collections import deque

line = deque(["Bob", "Charlie", "David"])
line.appendleft("Alice")
print(line)

tickets = deque(["Ticket #101", "Ticket #102", "Ticket #103"])
print(tickets.popleft())

history = deque(maxlen=3)
history.append("Page 1")
history.append("Page 2")
history.append("Page 3")
print(history)
history.append("Page 4")
print(history)



# heapq examples
import heapq

scores = [45, 12, 89, 5, 23]
sorted_scores = heapq.heapify(scores)
print(scores)
sorted_scores = heapq.heappop(scores)
print(sorted_scores)

issues = [10, 25, 40]
heapq.heapify(issues)
heapq.heappush(issues,4)
print(issues)

dataset = [100, 4, 23, 99, 56, 1004, 12]
print(heapq.nlargest(3, dataset))