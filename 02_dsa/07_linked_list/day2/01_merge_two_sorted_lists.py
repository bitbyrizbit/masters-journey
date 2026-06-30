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
    
def merge_sorted_lists(head1, head2):
    dummy = ListNode(0)
    tail = dummy
    while head1 and head2:
        if head1.val < head2.val:
            tail.next = head1
            head1 = head1.next
        else:
            tail.next = head2
            head2 = head2.next
        tail = tail.next
    tail.next = head1 if head1 else head2
    return dummy.next
        

head1 = build_linked_list([1,3,5])
head2 = build_linked_list([2,4,6])
result = merge_sorted_lists(head1, head2)
print_linked_list(result)
