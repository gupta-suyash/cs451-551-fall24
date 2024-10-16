from utilities.algorithms import binary_search, linear_search
from config import Config
from errors import *
import unittest

class Node:
    def __init__(self, minimum_degree=16, is_leaf: bool=False):
        assert(minimum_degree >= 2)
        self.minimum_degree = minimum_degree
        self.is_leaf: bool = is_leaf
        
        self.keys = []
        self.values = []

    """
    A maintained B+ Tree Node has multiple properties.
    This function checks if a node is maintained.
    Use for debuging.
    """
    def is_maintained(self, is_root) -> bool:
        if self.minimum_degree < 2:
            raise MinimumDegreeError(self.minimum_degree, self)
        
        if not is_root:
            if len(self.keys) < self.minimum_degree - 1:
                raise NonRootNodeKeyCountError(len(self.keys), self.minimum_degree - 1, self)

        if len(self.keys) > 2 * self.minimum_degree - 1:
            raise MaxKeysExceededError(len(self.keys), self)

        if self.is_leaf:
            if len(self.values) != len(self.keys):
                raise LeafNodeValueError(len(self.values), len(self.keys), self)
        else:
            if len(self.values) != len(self.keys) + 1:
                raise InternalNodeValueCountError(len(self.values), len(self.keys), self)
            
            for value in self.values:
                if not isinstance(value, Node):
                    raise InternalNodeTypeError(self)

        for i in range(1, len(self.keys)):
            if self.keys[i - 1] > self.keys[i]:
                raise NonDecreasingOrderError(self)

        return True
    
    def __str__(self):
        values = ["Node"] * len(self.values) if type(self.values[0]) is Node else self.values
        return f"Node(minimum_degree={self.minimum_degree}, keys={self.keys}, values={values})"

        

class TestNode(unittest.TestCase):

    def test_initialization(self):
        node = Node()
        self.assertEqual(node.minimum_degree, 16)
        self.assertFalse(node.is_leaf)
        self.assertEqual(node.keys, [])
        self.assertEqual(node.values, [])

        node = Node(minimum_degree=4, is_leaf=True)
        self.assertEqual(node.minimum_degree, 4)
        self.assertTrue(node.is_leaf)

    def test_is_maintained_leaf_node(self):
        node = Node(minimum_degree=2, is_leaf=True)
        node.keys = [1, 2, 3]
        node.values = [10, 20, 30]

        self.assertTrue(node.is_maintained(is_root=False))

    def test_is_maintained_internal_node(self):
        child_node1 = Node(minimum_degree=2, is_leaf=True)
        child_node2 = Node(minimum_degree=2, is_leaf=True)
        node = Node(minimum_degree=2, is_leaf=False)
        node.keys = [1]
        node.values = [child_node1, child_node2]

        self.assertTrue(node.is_maintained(is_root=False))

    def test_is_maintained_invalid_leaf_node(self):
        node = Node(minimum_degree=2, is_leaf=True)
        node.keys = [1, 2]
        node.values = [10]  # len(values) != len(keys)

        with self.assertRaises(LeafNodeValueError):
            node.is_maintained(is_root=False)

    def test_is_maintained_invalid_internal_node(self):
        child_node = Node(minimum_degree=2, is_leaf=True)
        node = Node(minimum_degree=2, is_leaf=False)
        node.keys = []
        node.values = [child_node]

        with self.assertRaises(NonRootNodeKeyCountError):
            node.is_maintained(is_root=False)

    def test_keys_order(self):
        node = Node(minimum_degree=2, is_leaf=False)
        node.keys = [1, 3, 2]  # This should be an invalid case
        node.values = [Node()] * 4

        with self.assertRaises(NonDecreasingOrderError):
            node.is_maintained(is_root=False)

    def test_keys_within_limits(self):
        node = Node(minimum_degree=2, is_leaf=False)
        node.keys = [1, 2, 3]
        node.values = [Node()] * 4

        self.assertTrue(node.is_maintained(is_root=False))

        node.keys = list(range(1, 10))  # 9 keys, invalid if minimum_degree is 5
        with self.assertRaises(MaxKeysExceededError):
            node.is_maintained(is_root=False)

        






class BPlusTree:
    """
    B+ Tree

    is_maintained() -> bool
    insert(key, value)
    get(key) -> value
    contains_key(key) -> bool
    minimum() -> value
    maximum() -> value
    remove(key)
    len() -> b+ tree length

    """
    def __init__(self, minimum_degree: int=Config.b_plus_tree_minimum_degree, debug_mode: bool=False):
        self.height = 0
        self.length = 0
        self.minimum_degree = minimum_degree
        self.search_algorithm_threshold = Config.b_plus_tree_search_algorithm_threshold
        self.root = Node(minimum_degree)
        # TODO: maintain a self.link if the node is a leaf for efficient range queries.

        # TODO: Debug Mode.
        # When True, everytime a node is visited, call node.is_maintained()
        # Also check that all leaves are at the same height.
        self.debug_mode = debug_mode 
        # self.unique = unique # Eventually I think we should be able to control for this.

    def is_maintained(self):
        if not self.root.is_maintained(is_root=True):
            print("root node is not maintained")
            return False
        
        # Check if all leaves are at the same height
        leaf_height = self._check_leaves_height(self.root, 0)
        if leaf_height is None:
            print("Leaf height is not balanced")
            return False
        return True

    def _check_leaves_height(self, node: Node, current_height: int):
        if not node.is_maintained(is_root=(current_height == 0)):
            print(f"Node with keys {node.keys} is not maintained")
            return None
        
        if node.is_leaf:
            # If it's a leaf node, return its height
            return current_height
    
        
        # If it's not a leaf, go through its children
        heights = []
        for child in node.values:
            if isinstance(child, Node):
                child_height = self._check_leaves_height(child, current_height + 1)
                if child_height is not None:
                    heights.append(child_height)

        # Check if all heights are the same
        if heights and all(h == heights[0] for h in heights):
            return heights[0]  # Return the common height
        else:
            return None  # Heights are inconsistent

    def insert(self, key, value):
        if self.length == 0:
            self.root = Node(self.minimum_degree, is_leaf=True)
            self.root.keys.append(key)
            self.root.values.append(value)
            self.length += 1
            return
        
        node = self.root
        path = []

        while not node.is_leaf:
            path.append(node)
            index = self._find_key_index(node.keys, key)

            if index < len(node.keys) and node.keys[index] < key:
                node = node.values[index + 1]
            else:
                node = node.values[index]

        index = self._find_key_index(node.keys, key)

        if index < len(node.keys) and node.keys[index] == key:
            node.values[index] = value
            return
        
        node.keys.insert(index, key)
        node.values.insert(index, value)
        self.length += 1

        if len(node.keys) == 2 * self.minimum_degree:
            self._split_leaf_node(node, path)

    def _split_leaf_node(self, leaf_node, path):
        new_leaf = Node(self.minimum_degree, is_leaf=True)
        
        # Move half the keys and values to the new leaf node
        mid_index = self.minimum_degree - 1
        new_leaf.keys = leaf_node.keys[mid_index:]
        new_leaf.values = leaf_node.values[mid_index:]

        # Update the original leaf node
        leaf_node.keys = leaf_node.keys[:mid_index]
        leaf_node.values = leaf_node.values[:mid_index]

        # If the leaf is the root, create a new root
        if leaf_node == self.root:
            new_root = Node(self.minimum_degree, is_leaf=False)
            new_root.keys.append(new_leaf.keys[0])  # Add the first key of the new leaf
            new_root.values.append(leaf_node)  # Left child
            new_root.values.append(new_leaf)  # Right child
            self.root = new_root
            self.height += 1
        else:
            # Insert the new key into the parent node
            parent_node = path[-1]
            index = self._find_key_index(parent_node.keys, new_leaf.keys[0])
            parent_node.keys.insert(index, new_leaf.keys[0])
            parent_node.values.insert(index + 1, new_leaf)

            # Split the parent node if necessary
            if len(parent_node.keys) == 2 * self.minimum_degree - 1:
                self._split_internal_node(parent_node)

    def _split_internal_node(self, internal_node):
        new_internal = Node(self.minimum_degree, is_leaf=False)
        
        mid_index = self.minimum_degree - 1
        new_internal.keys = internal_node.keys[mid_index + 1:]
        new_internal.values = internal_node.values[mid_index + 1:]

        # Update the original internal node
        internal_node.keys = internal_node.keys[:mid_index]
        internal_node.values = internal_node.values[:mid_index + 1]

        # If the internal node is the root, create a new root
        if internal_node == self.root:
            new_root = Node(self.minimum_degree, is_leaf=False)
            new_root.keys.append(internal_node.keys[-1])  # Promote the middle key
            new_root.values.append(internal_node)  # Left child
            new_root.values.append(new_internal)  # Right child
            self.root = new_root
            self.height += 1
        else:
            # Insert the promoted key into the parent node
            parent_node = self._find_parent(self.root, internal_node)
            index = self._find_key_index(parent_node.keys, internal_node.keys[-1])
            parent_node.keys.insert(index, internal_node.keys[-1])
            parent_node.values.insert(index + 1, new_internal)

            # Split the parent if necessary (recursive)
            if len(parent_node.keys) == 2 * self.minimum_degree - 1:
                self._split_internal_node(parent_node)

    def _find_parent(self, current_node, child_node):
        # Find the parent of a given child node
        if current_node.is_leaf:
            return None  # Return None for root or if child is the root itself

        for i, child in enumerate(current_node.values):
            if child == child_node:
                return current_node
            if not child.is_leaf:
                parent = self._find_parent(child, child_node)
                if parent:
                    return parent
        return None
    
    def _find_key_index(self, keys, key):
        if len(keys) < self.search_algorithm_threshold:
            return linear_search(keys, key)
        return binary_search(keys, key)
    
    def get(self, key):
        node = self.root
                
        while node:
            index = self._find_key_index(node.keys, key)

            if node.is_leaf:
                if index < len(node.keys) and node.keys[index] == key:
                    return node.values[index]
                else:
                    return None
                
            if index < len(node.keys) and node.keys[index] < key:
                node = node.values[index + 1]
            else:
                node = node.values[index]


    # TODO: impliment each of these
    def contains_key(self, key) -> bool:
        raise NotImplementedError

    def minimum(self) -> Node:
        raise NotImplementedError

    def maximum(self) -> Node:
        raise NotImplementedError

    def remove(self, key):
        # self.length -= 1 if node is successfully removed
        # self.height may need to be adjusted
        raise NotImplementedError

    def len(self):
        # return self.length
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def values(self):
        raise NotImplementedError
    

class TestBPlusTree(unittest.TestCase):
    def setUp(self):
        self.tree = BPlusTree(minimum_degree=2)

    # I used https://www.cs.usfca.edu/~galles/visualization/BPlusTree.html to help me design this. -Kai
    def test_tree_is_maintained(self):
        # Root Node
        self.tree.root.keys = [7]
        
        # Internal Nodes
        internal1 = Node(2, False)
        internal2 = Node(2, False)
        self.tree.root.values = [internal1, internal2]
        
        # Leaf Nodes
        leaf11 = Node(2, True)
        leaf12 = Node(2, True)
        leaf13 = Node(2, True)

        leaf21 = Node(2, True)
        leaf22 = Node(2, True)

        internal1.keys = [3, 5]
        internal1.values = [leaf11, leaf12, leaf13]

        internal2.keys = [9]
        internal2.values = [leaf21, leaf22]

        # Leaf Node values
        leaf11.keys = [1, 2]
        leaf11.values = [1, 2]

        leaf12.keys = [3, 4]
        leaf12.values = [3, 4]

        leaf13.keys = [5, 6]
        leaf13.values = [5, 6]

        leaf21.keys = [7, 8]
        leaf21.values = [7, 8]

        leaf22.keys = [9, 10]
        leaf22.values = [9, 10]

        self.assertTrue(self.tree.is_maintained())

    def test_generated_tree_is_maintained(self):
        tree = self.tree
        for i in range(1, 11):
            tree.insert(i, i)

        self.assertTrue(self.tree.is_maintained())
        
        

