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

INDIRECTION_COLUMN = 0
RID_COLUMN = 1
TIMESTAMP_COLUMN = 2
SCHEMA_ENCODING_COLUMN = 3


class Record:

    def __init__(self, rid, key, columns):
        self.rid = rid
        self.key = key
        self.columns = columns

class Table:

    """
    :param name: string         #Table name
    :param num_columns: int     #Number of Columns: all columns are integer
    :param key: int             #Index of table key in columns
    """
    def __init__(self, name, num_columns, primary_key):
        self.name = name
        self.key = primary_key + Config.column_data_offset
        self.num_columns = num_columns
        self.page_directory = []
        self.index = Index(self)

        # Very rough implementaion of base and tail coupling, consider changing later

        for i in range(0, num_columns+4):
            self.page_directory.append({'Base':[Page()], 'Tail':[Page()]})

        
    def get_column(self, column_index):
        if column_index >= self.num_columns or column_index < 0:
            raise ColumnDoesNotExist
        return self.page_directory[column_index]

    def __merge(self):
        print("merge is happening")
        pass
 
