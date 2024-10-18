"""TABLE ERRORS"""
class TableNotUniqueError(Exception):
    def __init__(self, message="A Table must have a unique name"):
        self.message = message
        super().__init__(self.message)

class TableDoesNotExistError(Exception):
    def __init__(self, message="The table does not exist"):
        self.message = message
        super().__init__(self.message)

"""PAGE ERRORS"""
class PageNoCapacityError(Exception):
    def __init__(self, message="Page does not have enough capacity to write to"):
        self.message = message
        super().__init__(self.message)

class PageValueTooLargeError(Exception):
    def __init__(self, cell_size, value_thats_too_large):
        self.message = f"The value `{value_thats_too_large}` is too large for a {cell_size} byte page cell"
        super().__init__(self.message)

class PageKeyError(Exception):
    def __init__(self, key):
        self.message = "key `{key}` points to an uninitialized or invalid page location"
        super().__init__(self.message)

class ColumnDoesNotExist(Exception):
    def __init__(self,column_index, num_columns):
        self.column_index = column_index
        self.num_columns = num_columns
        super().__init__(f'Column index {self.column_index} does not exist, table has {self.num_columns} columns')

"""B+TREE ERRORS"""
# bptree_exceptions.py

class BPlusTreeError(Exception):
    """Base class for exceptions in B+ Tree."""
    pass

class MinimumDegreeError(BPlusTreeError):
    def __init__(self, minimum_degree, node):
        self.minimum_degree = minimum_degree
        self.node = node
        super().__init__(f"Node is NOT maintained: minimum_degree is {self.minimum_degree} for node {self.node}")

class LeafNodeValueError(BPlusTreeError):
    def __init__(self, values_count, keys_count, node):
        self.values_count = values_count
        self.keys_count = keys_count
        self.node = node
        super().__init__(f"Node is NOT maintained: Leaf node has {self.values_count} values and {self.keys_count} keys for node {self.node}")

class InternalNodeValueCountError(BPlusTreeError):
    def __init__(self, values_count, keys_count, node):
        self.values_count = values_count
        self.keys_count = keys_count
        self.node = node
        super().__init__(f"Node is NOT maintained: Internal node has {self.values_count} values and {self.keys_count} keys for node {self.node}")

class InternalNodeTypeError(BPlusTreeError):
    def __init__(self, node):
        self.node = node
        super().__init__(f"Node is NOT maintained: Internal node value is not a Node for node {self.node}")

class NonRootNodeKeyCountError(BPlusTreeError):
    def __init__(self, keys_count, minimum_required, node):
        self.keys_count = keys_count
        self.minimum_required = minimum_required
        self.node = node
        super().__init__(f"Node is NOT maintained: Non-root node has {self.keys_count} keys, less than minimum required ({self.minimum_required}) for node {self.node}")

class MaxKeysExceededError(BPlusTreeError):
    def __init__(self, keys_count, node):
        self.keys_count = keys_count
        self.node = node
        super().__init__(f"Node is NOT maintained: Node has {self.keys_count} keys, exceeding maximum for node {self.node}")

class NonDecreasingOrderError(BPlusTreeError):
    def __init__(self, node):
        self.node = node
        super().__init__(f"Node is NOT maintained: Keys are not in non-decreasing order for node {self.node}")

class UnbalancedTreeError(BPlusTreeError):
    def __init__(self, node):
        self.node = node
        super().__init__(f"B+ Tree is NOT maintained: The tree is unbalanced. All leaves are not at the same height")

class NonUniqueKeyError(BPlusTreeError):
    def __init__(self, key):
        super().__init__(f"Attempted to insert the existing key {key} in B+ Tree Unique Key Mode")