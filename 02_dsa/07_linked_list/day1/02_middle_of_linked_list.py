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

    
def middle_linked_list(head):
    if not head:
        return None
    count = 0 
    temp = head
    while temp:
        temp = temp.next 
        count += 1
    target = count // 2
    curr = head
    counter = 0 
    while counter < target:
        curr = curr.next 
        counter += 1
    return curr.val

head = build_linked_list([1,2,3,4,5])
result = middle_linked_list(head)
print(result)