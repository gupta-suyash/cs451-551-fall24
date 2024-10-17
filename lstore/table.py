from lstore.index import Index
from time import time

import config
from storage.page_dir import PageDirectory

INDIRECTION_COLUMN = 0  # Base: RID of latest tail; Tail: RID of prev
RID_COLUMN = 1  # Record ID (and index/location/hashable in page directory)
TIMESTAMP_COLUMN = 2  # Timestamp for both base and tail record
SCHEMA_ENCODING_COLUMN = 3  # Bits representing cols, 1s where updated


class Record:
    """Data record (not metadata)
    :param rid:      # Record ID
    :param key:      # Primary key value
    :param columns:  # Data in record's columns (including key)
    """

    def __init__(self, rid, key, columns):
        self.rid = rid
        self.key = key
        self.columns = columns


class Table:
    """
    :param name:         # Table name
    :param num_columns:  # Number of columns: all columns are integer
    :param key:          # Index of table key in columns (ie primary key, ex 2 if 3rd col)
    """

    def __init__(self, name: str, num_columns: int, key: int):
        if key >= num_columns:
            raise IndexError("Key index is greater than the number of columns")

        self.name = name
        self.num_columns = num_columns
        self.key = key

        # Given RID, returns records
        self.page_directory = PageDirectory(
            num_columns=num_columns,
            buffer_size=None, #config.MAX_BUFFER_SIZE
        )

        self.index = Index(num_columns)

    def __merge(self):
        print("merge is happening")
