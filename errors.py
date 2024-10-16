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
    def __init__(self, message="value size is larger than the page cell size"):
        self.message = message
        super().__init__(self.message)

class PageKeyError(Exception):
    def __init__(self, message="key points to an invalid page location"):
        self.message = message
        super().__init__(self.message)

"""B+TREE ERRORS"""
# bptree_exceptions.py

class BPlusTreeError(Exception):
    """Base class for exceptions in B+ Tree."""
    pass

class MinimumDegreeError(BPlusTreeError):
    def __init__(self, minimum_degree, node):
        self.minimum_degree = minimum_degree
        self.node = node
        super().__init__(f"Node maintenance failed: minimum_degree is {self.minimum_degree} for node {self.node}")

class LeafNodeValueError(BPlusTreeError):
    def __init__(self, values_count, keys_count, node):
        self.values_count = values_count
        self.keys_count = keys_count
        self.node = node
        super().__init__(f"Node maintenance failed: Leaf node has {self.values_count} values and {self.keys_count} keys for node {self.node}")

class InternalNodeValueCountError(BPlusTreeError):
    def __init__(self, values_count, keys_count, node):
        self.values_count = values_count
        self.keys_count = keys_count
        self.node = node
        super().__init__(f"Node maintenance failed: Internal node has {self.values_count} values and {self.keys_count} keys for node {self.node}")

class InternalNodeTypeError(BPlusTreeError):
    def __init__(self, node):
        self.node = node
        super().__init__(f"Node maintenance failed: Internal node value is not a Node for node {self.node}")

class NonRootNodeKeyCountError(BPlusTreeError):
    def __init__(self, keys_count, minimum_required, node):
        self.keys_count = keys_count
        self.minimum_required = minimum_required
        self.node = node
        super().__init__(f"Node maintenance failed: Non-root node has {self.keys_count} keys, less than minimum required ({self.minimum_required}) for node {self.node}")

class MaxKeysExceededError(BPlusTreeError):
    def __init__(self, keys_count, node):
        self.keys_count = keys_count
        self.node = node
        super().__init__(f"Node maintenance failed: Node has {self.keys_count} keys, exceeding maximum for node {self.node}")

class NonDecreasingOrderError(BPlusTreeError):
    def __init__(self, node):
        self.node = node
        super().__init__(f"Node maintenance failed: Keys are not in non-decreasing order for node {self.node}")
