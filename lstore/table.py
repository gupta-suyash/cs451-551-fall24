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

class PageDirectory:
    def __init__(self, num_columns):
        self.num_records = 0
        self.num_tail_records = 0
        self.num_columns = num_columns
        self.data = []
        for _ in range(0, num_columns):
            self.data.append({'Base':[], 'Tail':[]})

        

    def add_record(self, columns, tail_flg = 0):
        """
        Accepts list of column values and adds the values to the latest base page of each column
        """
        assert len(columns) == self.num_columns

        page_class = 'Base' if tail_flg == 0 else 'Tail'

        for i, column_value in enumerate(columns):
            # allocate new base page if we are at full capacity
            if (not self.data[i][page_class]) or (not self.data[i][page_class][-1].has_capacity()):
                self.data[i][page_class].append(Page())
            self.data[i][page_class][-1].write(column_value)

        if tail_flg == 0:
            self.num_records += 1
        else:
            self.num_tail_records += 1

    def get_rid_for_version(self, rid, relative_version = 0):
        """
        Find the value rid corresponding to specified version, provided the rid in the base page
        Returns rid and flag whether it is in base or tail
        """
        assert rid < self.num_records
        
        # IMPORTANT TODO: this works for 64 bit integers, need to make some smart function for variable data types
        page_capacity = Config.page_size // 8
        current_rid = rid
        page_num = current_rid // page_capacity
        order_in_page = current_rid % page_capacity

        schema = self.data[Config.schema_encoding_column_idx]['Base'][page_num].read(order_in_page)
        indirection = self.data[Config.indirection_column_idx]['Base'][page_num].read(order_in_page)

        # return base record if there is only one version
        if indirection == -1: 
            return 0, current_rid

        # get the latest version first
        current_rid = indirection
        
        page_num = current_rid // page_capacity
        order_in_page = current_rid % page_capacity

        # from now on we are definetely working with tail
        schema = self.data[Config.schema_encoding_column_idx]['Tail'][page_num].read(order_in_page)
        indirection = self.data[Config.indirection_column_idx]['Tail'][page_num].read(order_in_page)
        
        # get the relative version by iterating backwards using the indirection pointer
        # we stop either if we reached the specified relative version or the primary tail record (in this case we return the base record)
        version = 0
        while version > relative_version and indirection != -1:
            current_rid = indirection
            
            page_num = current_rid // page_capacity
            order_in_page = current_rid % page_capacity

            # from now on we are definetely working with tail
            schema = self.data[Config.schema_encoding_column_idx]['Tail'][page_num].read(order_in_page)
            indirection = self.data[Config.indirection_column_idx]['Tail'][page_num].read(order_in_page)
            version -= 1

        if version == relative_version:
            # return record from the tail
            return 1, current_rid
        
        elif indirection == -1:
            return 0, current_rid

        assert 1 == 0 # shouldn't reach this part

        pass
    
    def get_column_value(self, rid, column_id, tail_flg = 0):
        assert column_id < self.num_columns

        page_capacity = Config.page_size // 8
        page_num = rid // page_capacity
        order_in_page = rid % page_capacity

        if tail_flg == 0:
            assert rid < self.num_records
            return self.data[column_id]['Base'][page_num].read(order_in_page)
        else:
            assert rid < self.num_tail_records
            return self.data[column_id]['Tail'][page_num].read(order_in_page)
        
    def set_column_value(self, rid, column_id, tail_flg = 0):
        assert column_id < self.num_columns

        page_capacity = Config.page_size // 8
        page_num = rid // page_capacity
        order_in_page = rid % page_capacity

        if tail_flg == 0:
            assert rid < self.num_records
            return self.data[column_id]['Base'][page_num].read(order_in_page)
        else:
            assert rid < self.num_tail_records
            return self.data[column_id]['Tail'][page_num].read(order_in_page)
    
    def get_tail_column_value(self, rid, column_id):
        assert column_id < self.num_columns

        page_capacity = Config.page_size // 8
        page_num = rid // page_capacity
        order_in_page = rid % page_capacity

        return self.data[column_id]['Tail'][page_num].read(order_in_page)






class Table:

    def __init__(self, name, num_columns, primary_key):
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
        if (primary_key >= num_columns):
            # TODO: Raise an error since this should not be possible
            pass

        # Validate that the total number of columns is greater than 0
        if (num_columns <= 0):
            # TODO: Raise an error
            pass

        # Set internal state
        self.name = name

        self.key = primary_key + Config.column_data_offset
        self.num_columns = num_columns + Config.column_data_offset

        
        self.index = Index(self)

        self.page_directory = PageDirectory(num_columns + Config.column_data_offset)

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
    
    def add_base_page(self, column_index):
        if column_index >= self.num_columns or column_index < 0:
            raise ColumnDoesNotExist(column_index, self.num_columns)
        self.page_directory[column_index]['Base'].append(Page())

    def __merge(self):
        print("merge is happening")
        pass
 
