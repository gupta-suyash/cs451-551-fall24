"""
A centralized spot to configure the database.
"""
# from data_structures.b_plus_tree import BPlusTree
from data_structures.binary_search_tree import BSTree
# from data_structures.hash_map import HashMap

class Config:
    page_size = 2**12    #4KB
    page_cell_size = 8   # Thats what the adssignment description said.
    index_data_structure = BSTree     # Make sure this datastructure- 1: works  2: impliments get(key), get_range(low_key, high_key), insert(key, value)
    b_plus_tree_minimum_degree = 2**7   #128
    lstore_is_cumulative = False


    @staticmethod
    def display_config():
        """Method to display current configuration settings"""
        # Grow this method as more is added to this class.

        print(f"Page Size: {Config.page_size}")
        print(f"Page Cell Size: {Config.page_cell_size}")
        print(f"Index data structure: {Config.index_data_structure.__name__}")
        print(f"B+ Tree minimum degree: {Config.b_plus_tree_minimum_degree}")
        print(f"L-Store is Cumulative")