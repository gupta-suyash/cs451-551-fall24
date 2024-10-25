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
        self.maintenance_lists = [[] * table.num_columns] # Used for lazy index maintenance

        # Make an unordered index for the primary key
        self.create_index(table.primary_key, self.UnorderedDataStructure)
        

    def locate(self, column: int, value):
        """
        returns the location of all records with the given value on column "column"
        """
        self._apply_maintenance(column)

        if self.indices.get(column):
            index = self.indices[column]
            return index.get(value)
        else:
            return list(self._locate_linear(column, target_value=value))



    def locate_range(self, begin, end, column):
        """
        Returns the RIDs of all records with values in column "column" between "begin" and "end"
        """
        self._apply_maintenance(column)

        if self.indices.get(column):
            index = self.indices[column]
            return index.get_range(begin, end)
        else:
            return list(self._locate_range_linear(column, low_target_value=begin, high_target_value=end))


    def create_index(self, column_number, DataStructure=Config.index_ordered_data_structure):
        """
        Create index on specific column
        """
        if self.indices[column_number] is not None:
            raise ValueError("Index at column ", column_number, " already exists")
        
        # Initialize the data structure but still hold off on inserting values.
        self.indices[column_number] = DataStructure()
        self.maintenance_lists[column_number] = [(value, rid) for rid, value in enumerate(self.table.column_iterator())]


    def drop_index(self, column_number):
        """
        Drop index of specific column
        """
        self.indices[column_number] = None
    
    def _locate_linear(self, column, target_value):
        """
        Returns the rid of every row with target_value in a column
        A linear scan point query
        """
        for rid, value in enumerate(self.table.column_iterator(column)):
            if value == target_value:
                yield rid

    def _locate_range_linear(self, column, low_target_value, high_target_value):
        """
        Returns the rid of every row with a value within range in a column
        A linear scan range query
        """
        for rid, value in enumerate(self.table.column_iterator(column)):
            if value >= low_target_value and value <= high_target_value:
                yield rid
    
    def maintain_insert(self, row, rid):
        for column, value in enumerate(row):
            if self.indices[column]:
                self.maintenance_lists[column].append(value)

    def maintain_delete(self, rid):
        raise NotImplementedError
    
    def _apply_maintenance(self, column):
        maintenance_list = self.maintenance_lists[column]

        if maintenance_list == []:
            return

        index = self.indices[column]

        if not index:
            maintenance_list = []
            return

        if type(index) is self.OrderedDataStructure:
            maintenance_list.sort(key=lambda item: item[0])     # Sort by key

        for item in maintenance_list:
            index.insert(item[0], item[1])

        maintenance_list = []
