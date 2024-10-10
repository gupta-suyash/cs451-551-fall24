from data_structures.binary_search_tree import BSTree

"""
A data strucutre holding indices for various columns of a table. Key column should be indexd by default, other columns can be indexed through this object. Indices are usually B-Trees, but other data structures can be used as well.
"""

POINT_QUERY = 0
RANGE_QUERY = 1

class Index:

    def __init__(self, table):
        # One index for each column. All our empty initially.
        self.indices = [None] *  table.num_columns
        
        # Make an index for the primary key.
        # self.create_index(table.key)

        # Record how often queries are performed against each column.
        # We can then create and delete indices accordingly.
        self.usage_histogram = [[0, 0]] * table.num_columns
        

    """
    # returns the location of all records with the given value on column "column"
    """

    def locate(self, column, value):
        self.usage_histogram[column][POINT_QUERY] += 1
        raise NotImplementedError

    """
    # Returns the RIDs of all records with values in column "column" between "begin" and "end"
    """

    def locate_range(self, begin, end, column):
        self.usage_histogram[column][RANGE_QUERY] += 1
        raise NotImplementedError

    """
    # optional: Create index on specific column
    """

    def create_index(self, column_number, DataStructure=BSTree):
        if self.indices[column_number] is not None:
            raise ValueError("Index at column ", column_number, " already exists")

        self.indices[column_number] = DataStructure()
        raise NotImplementedError

    """
    # optional: Drop index of specific column
    """

    def drop_index(self, column_number):
        self.indices[column_number] = None
        raise NotImplementedError
