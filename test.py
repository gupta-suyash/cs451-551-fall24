from lstore.db import Database
from lstore.query import Query

db = Database()

grades_table = db.create_table('Grades', 5, 0)

query = Query(grades_table)

print(type(query.table))

query.insert(*[0,1,2,3,4])