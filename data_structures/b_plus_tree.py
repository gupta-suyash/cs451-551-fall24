from utilities.algorithms import binary_search
from config import Config

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
        self.root = Node(minimum_degree)

        # TODO: Debug Mode.
        # When True, everytime a node is visited, call node.is_maintained()
        # Also check that all leaves are at the same height.
        self.debug_mode = debug_mode 
        # self.unique = unique # Eventually I think we should be able to control for this.

    def is_maintained(self):
        # Every node in BPlusTree passes node.is_maintained()
        # All leaves have the same depth: self.height
        raise NotImplementedError

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
    




def test_b_plus_tree_node():
    # Test case 1: Valid internal node
    internal_node = Node(minimum_degree=3, is_leaf=False)
    internal_node.keys = [10, 20]
    internal_node.values = [Node()] * 3
    assert internal_node.is_maintained(is_root=False), "Test Case 1 Failed"


    # Test case 2: Valid leaf node
    leaf_node = Node(minimum_degree=3, is_leaf=True)
    leaf_node.keys = [5, 15]
    leaf_node.values = ["hello", "world"]
    assert leaf_node.is_maintained(is_root=True), "Test Case 2 Failed"

    # Test case 3: Root node with 1 key (valid case)
    root_node = Node(minimum_degree=3, is_leaf=False)
    root_node.keys = [30]
    root_node.values = [Node()] * 2
    assert root_node.is_maintained(is_root=True), "Test Case 3 Failed"

    # Test case 4: Internal node with too few keys
    bad_internal_node = Node(minimum_degree=3, is_leaf=False)
    bad_internal_node.keys = []
    bad_internal_node.values = [Node()]  # Invalid since it should have at least minimum_degree - 1 keys
    assert not bad_internal_node.is_maintained(is_root=False), "Test Case 4 Failed"

    # Test case 5: Leaf node with too many keys
    bad_leaf_node = Node(minimum_degree=3, is_leaf=True)
    bad_leaf_node.keys = [5, 15, 25, 35, 45, 55]  # More than 2 * minimum_degree - 1 keys
    assert not bad_leaf_node.is_maintained(is_root=False), "Test Case 5 Failed"
    
    # Test case 6: Non-decreasing order of keys
    bad_order_node = Node(minimum_degree=3, is_leaf=False)
    bad_order_node.keys = [10, 5]  # Not in non-decreasing order
    bad_order_node.values = [Node()] * 3
    assert not bad_order_node.is_maintained(is_root=False), "Test Case 6 Failed"

    # Test case 7: Valid leaf node with 0 keys
    empty_leaf_node = Node(minimum_degree=3, is_leaf=True)
    empty_leaf_node.keys = []
    assert empty_leaf_node.is_maintained(is_root=True), "Test Case 7 Failed"

    print("All test cases passed!")

# test_b_plus_tree_node()


