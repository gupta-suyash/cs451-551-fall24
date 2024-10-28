from lstore.db import Database
from lstore.query import Query
from lstore.page import Page
from sys import getsizeof

db = Database()

grades_table = db.create_table('Grades', 3, 0)
query = Query(grades_table)

query.insert(*[0,0,0])
query.update(0, *[1,1,None])

record = query.select(0, 0, [1,1,1])[0]
record.info_print()
