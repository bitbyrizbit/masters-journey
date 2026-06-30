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

def is_palindrome(head):
    fast = head 
    slow = head 
    while fast and fast.next:
        fast = fast.next.next 
        slow = slow.next 
    prev = None
    curr = slow
    while curr:
        nxt = curr.next  
        curr.next = prev 
        prev = curr      
        curr = nxt
    first_half = head
    second_half = prev
    while second_half:
        if first_half.val != second_half.val:
            return False
        first_half = first_half.next
        second_half = second_half.next
    return True

head = build_linked_list([1,2,3,2,1])
print(is_palindrome(head))
