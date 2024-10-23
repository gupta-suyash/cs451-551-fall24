from lstore.db import Database
from lstore.query import Query
from lstore.page import Page
from sys import getsizeof

test = Page()


test.write(8)
print(test.read(0))

'''
byte_arr = bytearray()
value=26
byte_rep = value.to_bytes(8)

byte_arr[0:8] = byte_rep

print(int.from_bytes(byte_arr[0:8]))
'''