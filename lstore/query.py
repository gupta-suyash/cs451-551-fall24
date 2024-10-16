from typing import Literal

from lstore.table import Table, Record
from lstore.index import Index


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

    def delete(self, primary_key) -> bool:
        """
        # internal Method
        # Read a record with specified RID
        # Returns True upon successful deletion
        # Return False if record doesn't exist or is locked due to 2PL
        """
        pass

    def insert(self, *columns) -> bool:
        """
        # Insert a record with specified columns
        # Return True upon succesful insertion
        # Returns False if insert fails for whatever reason
        """
        schema_encoding = '0' * self.table.num_columns  # TODO: use actual bits
        pass

    def select(
        self,
        search_key,
        search_key_index,
        projected_columns_index: list[Literal[0, 1]]
    ) -> list[Record] | False:
        """
        # Read matching record with specified search key
        # :param search_key: the value you want to search based on
        # :param search_key_index: the column index you want to search based on
        # :param projected_columns_index: what columns to return. array of 1 or 0 values.
        # Returns a list of Record objects upon success
        # Returns False if record locked by TPL
        # Assume that select will never be called on a key that doesn't exist
        """
        pass

    def select_version(self, search_key, search_key_index, projected_columns_index, relative_version):
        """
        # Read matching record with specified search key
        # :param search_key: the value you want to search based on
        # :param search_key_index: the column index you want to search based on
        # :param projected_columns_index: what columns to return. array of 1 or 0 values.
        # :param relative_version: the relative version of the record you need to retreive.
        # Returns a list of Record objects upon success
        # Returns False if record locked by TPL
        # Assume that select will never be called on a key that doesn't exist
        """
        pass

    def update(self, primary_key, *columns) -> bool:
        """
        # Update a record with specified key and columns
        # Returns True if update is succesful
        # Returns False if no records exist with given key or if the target record cannot be accessed due to 2PL locking
        """
        pass

    def sum(self, start_range, end_range, aggregate_column_index):
        """
        :param start_range: int         # Start of the key range to aggregate 
        :param end_range: int           # End of the key range to aggregate 
        :param aggregate_columns: int  # Index of desired column to aggregate
        # this function is only called on the primary key.
        # Returns the summation of the given range upon success
        # Returns False if no record exists in the given range
        """
        pass

    def sum_version(self, start_range, end_range, aggregate_column_index, relative_version):
        """
        :param start_range: int         # Start of the key range to aggregate 
        :param end_range: int           # End of the key range to aggregate 
        :param aggregate_columns: int  # Index of desired column to aggregate
        :param relative_version: the relative version of the record you need to retreive.
        # this function is only called on the primary key.
        # Returns the summation of the given range upon success
        # Returns False if no record exists in the given range
        """
        pass

    def increment(self, key, column):
        """
        increments one column of the record
        this implementation should work if your select and update queries already work
        :param key: the primary of key of the record to increment
        :param column: the column to increment
        # Returns True is increment is successful
        # Returns False if no record matches key or if target record is locked by 2PL.
        """
        r = self.select(key, self.table.key, [1] * self.table.num_columns)[0]
        if r is not False:
            updated_columns = [None] * self.table.num_columns
            updated_columns[column] = r[column] + 1
            u = self.update(key, *updated_columns)
            return u
        return False
