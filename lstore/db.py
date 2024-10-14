from lstore.table import Table

class Database():
    def __init__(self):
        self.tables = {} # Dictionary of name - Table pairs

    # Not required for milestone1
    def open(self, path):
        pass

    def close(self):
        pass

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
        if (self.tables[name] == None):
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

        if (self.tables[name]):
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
