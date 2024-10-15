from utilities.algorithms import binary_search, linear_search
from config import Config
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
        try:
            # minimum_degree >= 2
            assert(self.minimum_degree >= 2)

            # Leaf nodes have a value for every key
            # Internal nodes have one more value than keys
            if self.is_leaf:
                assert(len(self.values) == len(self.keys))
            else:
                assert(len(self.values) == len(self.keys) + 1)

            # Internal node values must be other nodes
            if not self.is_leaf:
                for value in self.values:
                    assert type(value) is Node

            # Every node other than the root must contain minimum_degree - 1 keys or greater.
            if not is_root:
                assert(len(self.keys) >= self.minimum_degree - 1)

            # Every node may contain at most 2 * minimum_degree - 1 keys.
            assert(len(self.keys) <= 2 * self.minimum_degree - 1)

            # keys must be in non-decreasing order
            for i in range(1, len(self.keys)):
                assert(self.keys[i - 1] <= self.keys[i])

            return True
        except AssertionError:
            return False
        

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
        node.values = [10]  # len(values) != len(keys) + 1

        self.assertFalse(node.is_maintained(is_root=False))

    def test_is_maintained_invalid_internal_node(self):
        child_node = Node(minimum_degree=2, is_leaf=True)
        node = Node(minimum_degree=2, is_leaf=False)
        node.keys = []
        node.values = [child_node]

        # Invalid because minimum_degree - 1 is not met
        self.assertFalse(node.is_maintained(is_root=False))

    def test_keys_order(self):
        # Test a node with non-decreasing order
        node = Node(minimum_degree=2, is_leaf=False)
        node.keys = [1, 3, 2]  # This should be an invalid case
        node.values = [Node()] * 4

        self.assertFalse(node.is_maintained(is_root=False))

    def test_keys_within_limits(self):
        node = Node(minimum_degree=2, is_leaf=False)
        node.keys = [1, 2, 3]
        node.values = [Node()] * 4

        self.assertTrue(node.is_maintained(is_root=False))

        # Test exceeding maximum keys
        node.keys = list(range(1, 10))  # 9 keys, invalid if minimum_degree is 5
        self.assertFalse(node.is_maintained(is_root=False))

        






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
            return False
        
        # Check if all leaves are at the same height
        leaf_height = self._check_leaves_height(self.root, 0)
        return leaf_height is not None

    def _check_leaves_height(self, node: Node, current_height: int):
        if not node.is_maintained(is_root=(current_height == 0)):
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

    def test_tree_is_maintained(self):
        self.tree.keys = [5, 10]
        self.tree.values = [Node(2), Node(2), Node(2)]
        self.tree.values[0].keys = [2]
        self.tree.values[0].values = [Node(2, True), Node(2, True)]
        self.tree.values[1].keys = [7]
        self.tree.values[1].values = [Node(2, True), Node(2, True)]
        self.tree.values[2].keys = [12]
        self.tree.values[2].values = [Node(2, True), Node(2, True)]

        self.assertTrue(self.tree.is_maintained())
