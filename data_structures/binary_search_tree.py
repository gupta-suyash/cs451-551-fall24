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
    """
    Binary Search Tree.
    You can use this as a dictionary!

    Operations:
    insert - O(lg(h))
    get - O(lg(h))
    contains_key - O(lg(h))
    minimum - O(lg(h))
    maximum - O(lg(h))
    remove - O(lg(h))
    len - O(1)
    keys - O(nlg(h)) i'm pretty sure
    """


    def __init__(self, unique: bool=True):
        self.root = None
        self.length = 0
        self.unique = unique
    
    # TODO: make sure this handles collisions gracefully. Le
    def insert(self, key, value) -> bool:
        self.length += 1
        new_node = Node(key, value)
        parent_node = None
        node = self.root

        while node is not None:
            parent_node = node
            if self.unique and new_node.key == node.key:
                return False

            if new_node.key < node.key:
                node = node.left
            else:
                node = node.right

        new_node.parent = parent_node

        if parent_node is None:
            self.root = new_node
        elif new_node.key < parent_node.key:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        return True

    # TODO: if not unique keys, get the key node value, then node = node.successor while node.key == key.
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
    
    def keys(self):
        if self.root is None:
            return None
        
        node: Node = self.root.minimum()
        keys = []

        while node is not None:
            keys.append(node.key)
            node = node.successor()
            

        return keys