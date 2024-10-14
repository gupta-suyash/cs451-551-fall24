"""
The Index class provides a data structure that allows fast processing of queries (e.g., select or 
update) by indexing columns of tables over their values. Given a certain value for a column, the 
index should efficiently locate all records having that value. The key column of all tables is 
required to be indexed by default for performance reasons. However, supporting secondary indexes 
is optional for this milestone. The API for this class exposes the two functions create_index and 
drop_index (optional for this milestone)
"""

from data_structures.binary_search_tree import BSTree
from config import Config

POINT_QUERY = 0
RANGE_QUERY = 1

class Index:
    """
    A data strucutre holding indices for various columns of a table. Key column should be indexd by default, other columns can be indexed through this object. Indices are usually B-Trees, but other data structures can be used as well.
    """
    def __init__(self, table):
        # One index for each column. All are empty initially.
        self.indices = [None] *  table.num_columns
        self.DataStructure = Config.index_data_structure

        # Table owns and Index and Index has a reference to that table that owns it.
        self.table = table

        #
        
        # Make an index for the primary key.
        # self.create_index(table.key)

        # Record how often queries are performed against each column.
        # We can then create and delete indices accordingly.
        self.usage_histogram = [[0, 0]] * table.num_columns
        

    def locate(self, column: int, value):
        """
        returns the location of all records with the given value on column "column"
        """
        assert column < self.table.num_columns and column >= 0, "Index.locate should receive a valid column number"
        self.usage_histogram[column][POINT_QUERY] += 1

        if self.indices[column] is None:
            return self.__linear_scan(column)

        raise NotImplementedError


    def locate_range(self, begin, end, column):
        """
        Returns the RIDs of all records with values in column "column" between "begin" and "end"
        """
        self.usage_histogram[column][RANGE_QUERY] += 1
        raise NotImplementedError


    def create_index(self, column_number):
        """
        optional: Create index on specific column
        """
        if self.indices[column_number] is not None:
            raise ValueError("Index at column ", column_number, " already exists")
        

        self.indices[column_number] = self.DataStructure()
        print(self.table.name)

        # Pseudo code for how I imagine creating the index table.
        # for cell in self.table.column[column]:
        #     self.indices

        raise NotImplementedError


    def drop_index(self, column_number):
        """
        optional: Drop index of specific column
        """
        self.indices[column_number] = None
    

    def __linear_scan(self, column):
        """
        I'm pretty sure that if a column doesn't have an index, we need to linear scan the rows to locate a row. -Kai
        """
        raise NotImplementedError
