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

def detect_cycle_start(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next         
        fast = fast.next.next    
        if slow == fast:          
            fast = head
            while slow != fast:
                slow = slow.next 
                fast = fast.next
            return slow
    return None

head = build_linked_list([3,2,0,-4])
head.next.next.next.next = head.next

result = detect_cycle_start(head)
print(result.val if result else "None")
