"""
The Database class is a general interface to the database and handles high-level operations such as 
starting and shutting down the database instance and loading the database from stored disk files. 
This class also handles the creation and deletion of tables via the create and drop function. The 
create function will create a new table in the database. The Table constructor takes as input the 
name of the table, the number of columns, and the index of the key column. The drop function 
drops the specified table
"""

from lstore.table import Table
from errors import TableNotUniqueError

class Database():
    def __init__(self):
        self.tables = {} # Dictionary of name - Table pairs

    # Not required for milestone1
    def open(self, path):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def create_table(self, name, num_columns, key_index):
        """Creates a new table

        Parameters
        ----------
        name : str
            Table name
        num_columns : int
            Number of Columns: all columns are integer
        key : int
            Index of table key in columns

        Returns
        -------
        table : Table
            The newly created table

        Raises
        ------
        
        """

        table = Table(name, num_columns, key_index)
        # Check that the name doesn't exist already
        if (name in self.tables):
            # TODO: throw error
            pass
        else:
            self.tables[name] = table  # Assign the newly created table to the database
            return table

    
    def drop_table(self, name):
        """Deletes the specified table

        Parameters
        ----------
        name : str
            The name of the table to delete
        
        Raises
        ------
        
        """

        if (name in self.tables):
            del self.tables[name] # Remove the table from the database
        else:
            # TODO: Throw an error
            pass

    
    def get_table(self, name):
        """Returns table with the passed name

        Parameters
        ----------
        name : str
            The name of the table to get

        Returns
        -------
        table : Table
            The table that was found in the current database
            or `None` if not found.
        """

        return self.tables[name]
