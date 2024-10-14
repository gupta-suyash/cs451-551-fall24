"""
The Page class provides low-level physical storage capabilities. In the provided skeleton, each 
page has a fixed size of 4096 KB. This should provide optimal performance when persisting to 
disk, as most hard drives have blocks of the same size. You can experiment with different sizes. 
This class is mostly used internally by the Table class to store and retrieve records. While working 
with this class, keep in mind that tail and base pages should be identical from the hardware’s point 
of view. The config.py file is meant to act as centralized storage for all the configuration options
and the constant values used in the code. It is good practice to organize such information into a
Singleton object accessible from every file in the project. This class will find more use when 
implementing persistence in the next milestone.
"""
from config import Config
from errors import PageNoCapacityError
import sys

class Page:

    def __init__(self, page_size=Config.page_size, cell_size=Config.page_cell_size):
        self.num_records = 0
        self.data = bytearray(page_size)
        self.cell_size = cell_size

    def __locate(self, cell_position):
        return self.cell_size * cell_position
        

    def has_capacity(self):
        return Config.page_size >= (self.num_records + 1) * self.cell_size

    def write(self, value):
        # assert(getsizeof(value) == self.cell_size)
        start_index = self.__locate(self.num_records)

        if self.has_capacity():
            self.data[start_index:start_index+self.cell_size] = value
        else:
            raise PageNoCapacityError

        self.num_records += 1

        print(self.data[:100])


