class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        else:
            node.right = self._insert_recursive(node.right, key)
        return node

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node.key if node else None
        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

class SinglyLinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = SinglyLinkedListNode(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def search(self, value):
        current = self.head
        while current:
            if current.value == value:
                return current.value
            current = current.next
        return None

# Exemplo de uso corrigido:
if __name__ == "__main__":
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(8)
    bst.insert(1)
    bst.insert(4)

    print("Busca na Árvore de Busca Binária:")
    print(bst.search(4))  # Procurando o valor 4 na árvore

    sll = SinglyLinkedList()
    sll.append(10)
    sll.append(20)
    sll.append(30)

    print("\nBusca na Lista Simplesmente Encadeada:")
    print(sll.search(20))  # Procurando o valor 20 na lista
