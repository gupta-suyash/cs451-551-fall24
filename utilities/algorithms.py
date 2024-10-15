# Assumes that list is sorted.
# If target isn't found, this returns the index that it would be inserted into.
# If there are duplicate values == target in the lst, return the first one.
def binary_search(lst: list, target):
    left, right = 0, len(lst) - 1
    result = -1 
    
    while left <= right:
        mid = (left + right) // 2
        if lst[mid] < target:
            left = mid + 1
        elif lst[mid] > target:
            right = mid - 1
        else:
            result = mid  
            right = mid - 1

    return result if result != -1 else left 

# Same assumptions and output of binary search.
# For a small len(lst), this may be faster due to cache locality and branch prediction.
def linear_search(lst: list, target):
    i = 0
    while i < len(lst) and lst[i] < target:
        i += 1
    return i




import unittest

class TestAlgorithms(unittest.TestCase):
    
    def search_algorithms(self, lst, target):
        """ Helper function to test both search algorithms. """
        binary_result = binary_search(lst, target)
        linear_result = linear_search(lst, target)
        self.assertEqual(binary_result, linear_result)

    def test_found(self):
        self.search_algorithms([1, 2, 3, 4, 5], 3)
        self.search_algorithms([1, 2, 3, 4, 5], 1)
        self.search_algorithms([1, 2, 3, 4, 5], 5)

    def test_not_found(self):
        self.search_algorithms([1, 2, 3, 4, 5], 0)  
        self.search_algorithms([1, 2, 3, 4, 5], 6)  
        self.search_algorithms([1, 2, 3, 4, 5], 2.5)
        self.search_algorithms([1, 2, 3, 4, 5], 4.5)

    def test_empty_list(self):
        self.search_algorithms([], 1)  # Should return index 0

    def test_single_element(self):
        self.search_algorithms([1], 1) 
        self.search_algorithms([1], 0) 
        self.search_algorithms([1], 2) 

    def test_duplicates(self):
        self.search_algorithms([1, 2, 2, 2, 3], 2) 
        self.search_algorithms([1, 2, 2, 2, 3], 1) 
        self.search_algorithms([1, 2, 2, 2, 3], 3) 
        self.search_algorithms([1, 2, 2, 2, 3], 0) 
        self.search_algorithms([1, 2, 2, 2, 3], 2.5) 
        self.search_algorithms([1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3], 3)