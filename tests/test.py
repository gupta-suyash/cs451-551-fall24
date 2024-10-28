from lstore.db import Database
from lstore.query import Query
from lstore.page import Page
from sys import getsizeof

db = Database()

grades_table = db.create_table('Grades', 3, 0)
query = Query(grades_table)

query.insert(*[0,0,1])
query.update(0, *[1,1,None])
query.update(0, *[None, None, 2])
query.update(0, *[None, None, 3])

record = query.select(0, 0, [1,1,1])[0]
record.info_print()

