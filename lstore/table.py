"""
The Table class provides the core of our relational storage functionality. All columns are 64-bit
integers in this implementation. Users mainly interact with tables through queries. Tables provide 
a logical view of the actual physically stored data and mostly manage the storage and retrieval of 
data. Each table is responsible for managing its pages and requires an internal page directory that, 
given a RID, returns the actual physical location of the record. The table class should also manage 
the periodical merge of its corresponding page ranges.
"""


from lstore.index import Index
from time import time
from lstore.page import Page
from errors import ColumnDoesNotExist
from config import Config


class Record:

    def __init__(self, rid, key, columns):
        self.rid = rid
        self.key = key
        self.columns = columns

class Table:

    def __init__(self, name, num_columns, key):
        """Initialize a Table

        Parameters
        ----------
        name: string
            The name of the table
        num_columns: int
            The total number of columns to store in the table
        key: int
            The index of the column to use as the primary key
        
        Raises
        ------

        """

        # Validate that the primary key column is within the range of columns
        if (key >= num_columns):
            # TODO: Raise an error since this should not be possible
            pass

        # Validate that the total number of columns is greater than 0
        if (num_columns <= 0):
            # TODO: Raise an error
            pass

        # Set internal state
        self.name = name

        self.key = key + Config.column_data_offset
        self.num_columns = num_columns + Config.column_data_offset

        self.page_directory = []
        self.index = Index(self)

        # Very rough implementaion of base and tail coupling, consider changing later

        for i in range(0, num_columns + Config.column_data_offset):
            self.page_directory.append({'Base':[Page()], 'Tail':[Page()]})

    def __contains__(self, key):
        """Implements the contains operator
        
        Parameters
        ----------
        key : int
            The primary key to find within the table
        
        Returns
        -------
        b : bool
            Whether or not the primary key was found
        """

        # Search through the primary key column and try to find it
        v = self.index.locate(self.key, key)  # TODO: double check this is the correct column
        return (v is not None)

    def __getitem__(self, key):
        """Implements the get operator

        Parameters
        ----------
        key : int
            The primary key to find within the table

        Returns
        -------
        r : Record
            The found Record object

        Raises
        ------
        IndexError
        """

        #if (key in self):
        #    return self.index.locate(self.key)
        #else:
        #    raise IndexError("Key {} does not exist.".format(key))

        # Use the internal Index to find a record
        return self.index.locate(self.key, key)

        
    def get_column(self, column_index):
        if column_index >= self.num_columns or column_index < 0:
            raise ColumnDoesNotExist(column_index, self.num_columns)
        return self.page_directory[column_index]

    def __merge(self):
        print("merge is happening")
        pass
 
