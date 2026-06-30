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

def remove_nth_from_end(head, n):
    dummy = ListNode(0,head)
    fast = dummy
    slow = dummy
    for i in range(n + 1):
        fast = fast.next
    while fast:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next
    
    
head = build_linked_list([1,2,3,4,5])
n = 2
result = remove_nth_from_end(head, n)
print_linked_list(result)
