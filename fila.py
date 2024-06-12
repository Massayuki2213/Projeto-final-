class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class Fila:
    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, data):
        new_node = Node(data)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.data

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from an empty queue")
        return self.front.data

    def display(self):
        elements = []
        current = self.front
        while current:
            elements.append(current.data)
            current = current.next
        return elements
