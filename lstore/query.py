"""
The Query class provides standard SQL operations such as insert, select, update, delete, and sum. 
The select function returns all the records matching the search key (if any), and only the projected 
columns of the matching records are returned. The insert function will insert a new record in the 
table. All columns should be passed a non-NULL value when inserting. The update function 
updates values for the specified set of columns. The delete function will delete the record with the
specified key from the table. The sum function will sum over the values of the selected column for 
a range of records specified by their key values. We query tables by direct function calls rather 
than parsing SQL queries.
"""

from lstore.table import Table, Record
from lstore.index import Index
from config import Config

def create_bitmask(items):
    """Creates a bitmask representing the given items."""
    mask = 0
    for item in items:
        mask |= (1 << item)
    return mask

class Query:
    """
    # Creates a Query object that can perform different queries on the specified table 
    Queries that fail must return False
    Queries that succeed should return the result or True
    Any query that crashes (due to exceptions) should return False
    """
    def __init__(self, table):
        self.table = table
        pass

    
    """
    # internal Method
    # Read a record with specified RID
    # Returns True upon succesful deletion
    # Return False if record doesn't exist or is locked due to 2PL
    """
    def delete(self, primary_key):
        pass
    
    
    """
    # Insert a record with specified columns
    # Return True upon succesful insertion
    # Returns False if insert fails for whatever reason
    """
    def insert(self, *columns):
        # as is, this SHOULD insert a new record, however, this needs to be tested first

        # in general we should return the whole column, not just the first page TODO: fix this
        page_rid = self.table.get_column(Config.rid_column_idx)['Base'][0]
        page_schema = self.table.get_column(Config.schema_encoding_column_idx)['Base'][0]
        page_indirection = self.table.get_column(Config.indirection_column_idx)['Base'][0]

        rid = page_rid.num_cells
        page_rid.write(rid)
        page_schema.write(0)
        # let zero correspond to null pointer
        page_indirection.write(0)
        
        for i in range(len(columns)):
            page = self.table.get_column(i + Config.column_data_offset)['Base'][0]
            page.write(columns[i])

    
    """
    # Read matching record with specified search key
    # :param search_key: the value you want to search based on
    # :param search_key_index: the column index you want to search based on
    # :param projected_columns_index: what columns to return. array of 1 or 0 values.
    # Returns a list of Record objects upon success
    # Returns False if record locked by TPL
    # Assume that select will never be called on a key that doesn't exist
    """
    def select(self, search_key, search_key_index, projected_columns_index):
        return self.select_version(search_key, search_key_index, projected_columns_index, 0)

    
    """
    # Read matching record with specified search key
    # :param search_key: the value you want to search based on2
    # :param search_key_index: the column index you want to search based on
    # :param projected_columns_index: what columns to return. array of 1 or 0 values.
    # :param relative_version: the relative version of the record you need to retreive.
    # Returns a list of Record objects upon success
    # Returns False if record locked by TPL
    # Assume that select will never be called on a key that doesn't exist
    """
    def select_version(self, search_key, search_key_index, projected_columns_index, relative_version):
        # general idea:
        # if there is an index for this column:
        #     use index to find rids
        # else:
        #     use linear iteration through rid page directory to find corresponding rid's
        # for each found rid construct a Record object:
        #   go to final version of record with specified rid and get all the column values
        #   for _ in range(relative_version)
        #       go to the previous version of the record using pointer to prev version

        pass


    
    """
    # Update a record with specified key and columns
    # Returns True if update is succesful
    # Returns False if no records exist with given key or if the target record cannot be accessed due to 2PL locking
    """
    def update(self, primary_key, *columns):
        # general idea
        # use index to find rid
        # append the new record version to the tail page 
        # update schema for base and tail records
        # DANIEL QUESTION: do we even need schema for now? I dont seem to understand where is it used?
        # Update indirection column for latest tail version and for base record
        # DANIEL QUESTION WHAT SERVES AS PTR? Do we need another id for specific record in memory? to distinguish between tail and base records

        pass

    
    """
    :param start_range: int         # Start of the key range to aggregate 
    :param end_range: int           # End of the key range to aggregate 
    :param aggregate_columns: int  # Index of desired column to aggregate
    # this function is only called on the primary key.
    # Returns the summation of the given range upon success
    # Returns False if no record exists in the given range
    """
    def sum(self, start_range, end_range, aggregate_column_index):
        pass

    
    """
    :param start_range: int         # Start of the key range to aggregate 
    :param end_range: int           # End of the key range to aggregate 
    :param aggregate_columns: int  # Index of desired column to aggregate
    :param relative_version: the relative version of the record you need to retreive.
    # this function is only called on the primary key.
    # Returns the summation of the given range upon success
    # Returns False if no record exists in the given range
    """
    def sum_version(self, start_range, end_range, aggregate_column_index, relative_version):
        pass

    
    """
    incremenets one column of the record
    this implementation should work if your select and update queries already work
    :param key: the primary of key of the record to increment
    :param column: the column to increment
    # Returns True is increment is successful
    # Returns False if no record matches key or if target record is locked by 2PL.
    """
    def increment(self, key, column):
        r = self.select(key, self.table.key, [1] * self.table.num_columns)[0]
        if r is not False:
            updated_columns = [None] * self.table.num_columns
            updated_columns[column] = r[column] + 1
            u = self.update(key, *updated_columns)
            return u
        return False
