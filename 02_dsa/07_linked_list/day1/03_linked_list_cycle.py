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

def linked_list_cycle(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next         
        fast = fast.next.next    
        if slow == fast:          
            return True
    return False   

head = build_linked_list([1,2,3,4,5])
print(linked_list_cycle(head))
