class Node:
    def __init__(self, val: int, next: Node = None, random: Node = None):
        self.val = val
        self.next = next
        self.random = random

def copy_random_list(head: Node) -> Node:
    if not head:
        return None
    mapping = {}
    curr = head
    while curr:
        mapping[curr] = Node(curr.val)
        curr = curr.next
    curr = head
    while curr:
        copy_node = mapping[curr]
        copy_node.next = mapping.get(curr.next)
        copy_node.random = mapping.get(curr.random)
        curr = curr.next
    return mapping[head]

n1 = Node(7)
n2 = Node(13)
n3 = Node(11)
n1.next = n2
n2.next = n3
n2.random = n1
n3.random = n2

result = copy_random_list(n1)
print(result.val if result else "None")
print(result.next.random.val if result and result.next and result.next.random else "None")
