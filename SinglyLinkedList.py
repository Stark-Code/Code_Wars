import sys


class SLL_Node:
    def __init__(self, val):
        self.value = val
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.length = 0
        self.head = None
        self.tail = None

    def append(self, value):
        newNode = SLL_Node(value)
        if self.length == 0:
            self.head = newNode
            self.tail = self.head
            self.length = 1
        else:
            self.tail.next = newNode
            self.tail = newNode
            self.length += 1
        return self

    def pop(self, node=None) -> SLL_Node:
        if self.head is None: return None
        current = self.head
        newTail = current
        while current.next:
            newTail = current
            current = current.next
        self.tail = newTail
        self.tail.next = None
        self.length -= 1
        return current  # Removed item

    def popZero(self):
        if self.length == 0: return None
        currentHead = self.head
        self.head = currentHead.next
        currentHeadVal = currentHead.value
        del currentHead
        self.length -= 1
        return currentHeadVal

    def insertZero(self, value):
        if self.length == 0:
            self.append(value)
        else:
            newNode = SLL_Node(value)
            newNode.next = self.head
            self.head = newNode
            self.length += 1
        return self

    def get(self, index):
        if index < 0 or index >= self.length: return None
        counter = 0
        current = self.head
        while counter < index:
            current = current.next
            counter += 1
        return current.value

    def printList(self):
        current = self.head
        while current:
            print(current.value)
            current = current.next
        print('')


ssList = SinglyLinkedList()
ssList.append(1)
ssList.append(2)
ssList.append(3)

ssList.printList()

removed = ssList.pop()
ssList.printList()
print(f'popped: {removed.value}')

ssList.append(4)
ssList.printList()
removedZ = ssList.popZero()
ssList.printList()
print(removedZ, '\n')
ssList.insertZero('z')
ssList.printList()
getVal = ssList.get(2)
print(f'GetValue: {getVal}')