"""
The Database class is a general interface to the database and handles high-level operations such as 
starting and shutting down the database instance and loading the database from stored disk files. 
This class also handles the creation and deletion of tables via the create and drop function. The 
create function will create a new table in the database. The Table constructor takes as input the 
name of the table, the number of columns, and the index of the key column. The drop function 
drops the specified table
"""

from lstore.table import Table
from errors import NotUniqueError

class Database():

    def __init__(self):
        self.tables = {}
        pass

    # Not required for milestone1
    def open(self, path):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    """
    # Creates a new table
    :param name: string         #Table name
    :param num_columns: int     #Number of Columns: all columns are integer
    :param key: int             #Index of table key in columns
    """
    def create_table(self, name, num_columns, key_index):
        if self.contains_table(name): # I figure that db tables should have unique names. -Kai
            raise NotUniqueError

        table = Table(name, num_columns, key_index)
        self.tables.append(table)
        return table
    

    def contains_table(self, name: str) -> bool:
        return self.table[name] is not None

    
    """
    # Deletes the specified table
    """
    def drop_table(self, name):
        raise NotImplementedError

    
    """
    # Returns table with the passed name
    """
    def get_table(self, name):
        return self.table[name]
