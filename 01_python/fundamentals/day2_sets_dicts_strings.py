# set examples 
og_list = [1, 2, 2, 3, 4, 4, 4, 5]
unique_set = set(og_list)
print (unique_set)
even_set = set()
for i in range(1,11):
    if i % 2 == 0:
        even_set.add(i)
print (even_set)
unique_set.discard(6)
print(unique_set)

group_a = [1, 3, 5, 7, 9]
group_b = [2, 3, 5, 8, 9]
print(set(group_a) & set(group_b)) 

print(set(group_a) - set(group_b))



# dictionary examples
my_dict = {"milk": 2.50, "bread": 1.99, "eggs": 3.49}
my_dict.pop("milk")
print(my_dict)
print(my_dict.get("milk",0.0))

print(my_dict.keys())
print(my_dict.values())
print(my_dict.items())

student_grades = {"Alice": 90, "Bob": 85, "Charlie": 92}
for k,v in student_grades.items():
    print(f"Student: {k}, Grade: {v}")

input_domains = ["9001 ://leetcode.com", "50 yahoo.com"]
domain_dict = {}

for domain in input_domains:
    count_str, url = domain.split(" ")
    count = int(count_str)
    parts = url.split(".")
    for i in range(len(parts)):
        subdomain = ".".join(parts[i:])
        domain_dict[subdomain] = domain_dict.get(subdomain, 0) + count
output = []
for subdomain, total_count in domain_dict.items():
    output.append(f"{total_count} {subdomain}")
print(output)



# string examples
string1 = "DataStructures"
print(string1[4:])
print(string1[::-1])

string2 = "   too many spaces   "
print(string2.strip())

my_string = ["Python", "is", "great", "for", "DSA"]
print("-".join(my_string))

my_string2 = "John,Doe,30,Engineer"
print(my_string2.split(","))

s = "  the sky  is blue  "
print(" ".join(s.strip().split()[::-1]))