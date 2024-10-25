"""
The Index class provides a data structure that allows fast processing of queries (e.g., select or 
update) by indexing columns of tables over their values. Given a certain value for a column, the 
index should efficiently locate all records having that value. The key column of all tables is 
required to be indexed by default for performance reasons. However, supporting secondary indexes 
is optional for this milestone. The API for this class exposes the two functions create_index and 
drop_index (optional for this milestone)
"""

from data_structures.b_plus_tree import BPlusTree
from data_structures.hash_map import HashMap
from config import Config

POINT_QUERY = 0
RANGE_QUERY = 1

class Index:
    """
    Give the index a column and a target value, and the index will give you a list of row id's that match

    Don't forget to maintain the index using maintain_insert and maintain_delete.
    The index needs to be told when the table is changed.
    Take care of your index!!!
    """
    def __init__(self, table):
        # One index for each column. All are empty initially.
        self.indices = [None] *  table.num_columns
        self.OrderedDataStructure = Config.index_ordered_data_structure
        self.UnorderedDataStructure = Config.index_unordered_data_structure
        self.usage_histogram = [[0, 0]] * table.num_data_columns
        self.table = table # Table owns and Index and Index has a reference to that table that owns it.

        # Make an unordered index for the primary key
        self.create_index(table.primary_key, self.UnorderedDataStructure)
        

    def locate(self, column: int, value):
        """
        returns the location of all records with the given value on column "column"
        """
        if self.indices.get(column):
            index = self.indices[column]
            return index.get(value)
        else:
            return list(self._locate_linear(column, target_value=value))



    def locate_range(self, begin, end, column):
        """
        Returns the RIDs of all records with values in column "column" between "begin" and "end"
        """
        if self.indices.get(column):
            index = self.indices[column]
            return index.get_range(begin, end)
        else:
            return list(self._locate_range_linear(column, low_target_value=begin, high_target_value=end))


    def create_index(self, column_number, DataStructure):
        """
        Create index on specific column
        """
        if self.indices[column_number] is not None:
            raise ValueError("Index at column ", column_number, " already exists")
        

        self.indices[column_number] = DataStructure()
        for rid, value in self.table.column_iterator(column_number):
            self.indices[column_number].insert(value, rid)

        # TODO: impliment bulk insert for the data structures
        # self.indices[column_number].bulk_insert(list(self.table.column_iterator()))

        raise NotImplementedError


    def drop_index(self, column_number):
        """
        Drop index of specific column
        """
        self.indices[column_number] = None
    
    def _locate_linear(self, column, target_value):
        """
        Returns the rid of every instance of the target_value in a column
        """
        for rid, value in enumerate(self.table.column_iterator(column)):
            if value == target_value:
                yield rid

    def _locate_range_linear(self, column, low_target_value, high_target_value):
        """
        I'm pretty sure that if a column doesn't have an index, we need to linear scan the rows to locate a row. -Kai
        """
        for rid, value in enumerate(self.table.column_iterator(column)):
            if value >= low_target_value and value <= high_target_value:
                yield rid
    
    def maintain_insert(self, row, rid):
        for data_column, index in enumerate(self.indices):
            if index:
                index.insert(row[data_column], rid)

    def maintain_delete(self, rid):
        raise NotImplementedError
