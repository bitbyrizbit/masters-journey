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

def print_linked_list(head):
    curr = head
    while curr:
        print(curr.val, end=" -> ")
        curr = curr.next
    print("None")

def reverse_k_group(head, k):
    if not head or k == 1:
        return head
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for i in range(k):
            kth = kth.next
            if not kth:
                return dummy.next
        group_next = kth.next
        prev = group_next
        curr = group_prev.next
        for i in range(k):
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        temp = group_prev.next
        group_prev.next = kth
        group_prev = temp
        
head = build_linked_list([1,2,3,4,5])
k = 2
result = reverse_k_group(head, k)
print_linked_list(result)
