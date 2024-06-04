# bst.py

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert(self.root, key, value)

    def _insert(self, current_node, key, value):
        if key < current_node.key:
            if current_node.left is None:
                current_node.left = Node(key, value)
            else:
                self._insert(current_node.left, key, value)
        elif key > current_node.key:
            if current_node.right is None:
                current_node.right = Node(key, value)
            else:
                self._insert(current_node.right, key, value)
        else:
            current_node.value = value  # Se a chave já existe, atualiza o valor

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, current_node, key):
        if current_node is None:
            return None
        elif key == current_node.key:
            return current_node.value
        elif key < current_node.key:
            return self._search(current_node.left, key)
        else:
            return self._search(current_node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, current_node, key):
        if current_node is None:
            return current_node

        if key < current_node.key:
            current_node.left = self._delete(current_node.left, key)
        elif key > current_node.key:
            current_node.right = self._delete(current_node.right, key)
        else:
            if current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left

            temp_val = self._find_min(current_node.right)
            current_node.key = temp_val.key
            current_node.value = temp_val.value
            current_node.right = self._delete(current_node.right, temp_val.key)

        return current_node

    def _find_min(self, current_node):
        while current_node.left is not None:
            current_node = current_node.left
        return current_node

    def in_order_traversal(self):
        return self._in_order_traversal(self.root)

    def _in_order_traversal(self, current_node):
        res = []
        if current_node is not None:
            res = self._in_order_traversal(current_node.left)
            res.append((current_node.key, current_node.value))
            res = res + self._in_order_traversal(current_node.right)
        return res
