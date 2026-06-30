class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_linked_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    curr = head
    for val in values[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def get_intersection_node(head1, head2):
    p1 = head1
    p2 = head2
    while p1 != p2:
        p1 = p1.next if p1 else head2
        p2 = p2.next if p2 else head1
    return p1

head1 = build_linked_list([4,1])
head2 = build_linked_list([5,6,1])
intersect = build_linked_list([8,4,5])

head1.next.next = intersect
head2.next.next.next = intersect

result = get_intersection_node(head1, head2)
print(result.val if result else "None")