# This Binary Search Tree is Inspired by the pseudo code from CLRS Introduction to Algorithms.

class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.left: Node = None
        self.right: Node = None
        self.parent: Node = parent

    def minimum(self):
        node = self

        while node.left is not None:
            node = node.left

        return node
    
    def maximum(self):
        node = self
        
        while node.right is not None:
            node = node.right

        return node
    
    def get(self, key):
        node = self
        while node is not None and key != node.key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        
        if node is None:
            return None
        else:
            return node
        
    def successor(self):
        node = self

        if node.right is not None:
            return node.right.minimum()
        y = node.parent
        while y is not None and node == y.right:
            node = y
            y = y.parent
        return y


class BSTree:
    def __init__(self):
        self.root = None
        self.length = 0
        print("Binary Search Tree Created at ", __name__)
    

    def insert(self, key, value):
        self.length += 1
        z = Node(key, value)
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

    def get(self, key):
        if self.root is None:
            return None

        node = self.root.get(key)
        if node is None:
            return None
        
        return node.value


    def contains_key(self, key) -> bool:
        if self.root is None:
            return None
        
        return self.root.get(key) is not None
        
    def minimum(self):
        if self.root is None:
            return None
        
        return self.root.minimum().value
        
    def maximum(self):
        if self.root is None:
            return None
        
        return self.root.maximum().value 
    
    def __transplant(self, a: Node, b: Node):
        if a.parent is None:
            self.root = b
        elif a == a.parent.left:
            a.parent.left = b
        else:
            a.parent.right = b

        if b is not None:
            b.parent = a.parent

    def remove(self, key):
        self.length -= 1
        # Unless we don't remove an element so be careful.
        raise NotImplementedError
    
    def len(self):
        return self.length

    def delete(self, node):
        # self.__transplant(Node(1, 2), Node(3, 1))
        pass