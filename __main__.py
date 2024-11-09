from collections.abs import Callable
from typing import Optional
from lstore.db import Database
from lstore.query import Query
from time import process_time
import random

def timeit(message   : str,
           f         : Callable,
           query     : Callable,
           *args,
           tab_width : int = 40,
           **kwargs,
           ):
    """ 
    Time the function 
    Args:
        message: Message to display to user
        f: function to time
        query: query created from db (grades_table)
        *args: arguments to pass to the function
        tab_width: integer for tab width post message
        **kwargs: keyword arguments to function

    Returns:
        rval: return value from function f
    """
    start_time = process_time()
    rval = f(query, *args, **kwargs)
    end_time = process_time()
    print(f"{message + " took:":<{tab_width}} {(end_time - start_time):0.6f} seconds")
    return rval

def trivial_query(query   : Callable,
                  keys    : list[int],
                  n       : int       = 10000,
                  offset  : int       = 906659671,
                  columns : list[int] = [93,0,0,0],
                  ) -> Callable:
    """
    Trivial query function where we insert some dummy columns
    Args:
        query: the query object
        keys: Our list of keys
        n: number of rounds
        offset: some random offset seed
        columns: a constant dummy column

    Returns:
        keys: list of updated keys
    """
    for i in range(n):
        query.insert(offset+i, *columns)
        keys.append(offset+i)
    return keys

def trivial_update(query   : Callable,
                   n       : int                 = 10000,
                   keys    : list[int]           = [],
                   columns : Optional[list[int]] = None,
                   ) -> None:
    """
    Update the queries 
    Args:
        query: query object
        n: number of rounds 
        keys: list of keys
        columns: our input columns

    Returns:
        None
    """
    for _ in range(n):
        query.update(random.choice(keys), *(choice(columns)))
    return 

def trivial_select(query   : Callable,
                   n       : int           = 10000,
                   keys    : list[int]     = [],
                   columns : Optional[list[int]] = None,
                   ) -> None:
    """
    Testing select function by randomly selecting keys
    Args:
        query: query object
        n: number of rounds 
        keys: list of keys
        columns: our input columns

    Returns:
        None
    """
    for _ in range(n):
        query.select(random.choice(keys), *columns)
    return 

def aggregate(query  : Callable,
              n      : int = 10000,
              batch  : int = 100,
              offset : int = 906659671,
              ) -> None:
    """
    Aggregate checking function
    Tests the query.sum function

    Args:
        query: query object
        n: number of rounds 
        batch: batch size we work over
        offset: a seed offset
    Returns:
        None
    """
    for i in range(0,n,batch):
        _val = offset + i
        _end = _val + batch
        result = query.sum(_val, _end-1, random.randrange(0,5))
    return 

def delete_records(query     : Callable,
                   n         : int = 10000,
                   offset    : int = 906659671,
                   ) -> None:
    """
    Tests deleting queries

    Args:
        query: query object
        n: number of rounds
        offset: some random offset seed

    Returns:
        None
    """
    for i in range(n):
        query.delete(offset+i)
    return 

def main(n           : int = 10000,     # Number of iterations
         offset      : int = 906659671, # Random seed
         table_name  : str = "Grades",  # name of our table
         num_columns : int = 5,         # Number of 'grades'
         key_index   : int = 0,         # Our primary key
         ) -> None:
    """
    Our main testing function
    We will test different aspects of the program through here
    """
    columns = [93, 0, 0, 0]

    db = Database()
    grades_table = db.create_table(name, num_columns, key_index)
    query = Query(grades_table)
    keys = []

    keys = timeit(f"Inserting {n} records", trivial_query, 
                         query=query, n=n,
                         keys=keys, offset=offset, columns=columns) 

    # Create a dummy 5x5 matrix of columns
    # First is all Nones, then diagonal is randrange(0,100)
    N = 5
    update_cols = [ [None for _ in range(N)] for _ in range(N) ]
    for i in range(1,N):
        update_cols[i][i] = random.randrange(0,100)

    timeit("Updating 10k records", 
           trivial_update, query=query, n=n,
           keys=keys, columns=update_cols)

    sel_cols = (0, [1,1,1,1,1])
    timeit("Selecting 10k records", 
           trivial_select, query=query, n=n,
           keys=keys, columns=sel_cols)

    timeit("Aggregate 10k of 100 records batch", 
           aggregate, query=query, n=n,
           )
    timeit("Deleting 10k records", 
           delete_records, query=query, n=n,
           )

if __name__ == '__main__':
    main()
