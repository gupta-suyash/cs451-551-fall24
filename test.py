from lstore.db import Database
from lstore.query import Query
import unittest


class TestLstroreDB(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        self.test_table = self.db.create_table('Test', 5, 0)
        self.query = Query(self.test_table)  

    def tearDown(self):
        self.db = None
        self.test_table = None
        self.query = None 

    def test_single_insert(self):
        test_values = [0,1,2,3,4]
        self.query.insert(*test_values)
        
        record = self.query.select(0, 0, [1,1,1,1,1])[0]

        self.assertListEqual(test_values, record.columns)

    def test_single_update(self):
        test_values = [0,1,2,3,4]
        self.query.insert(*test_values)

        self.query.update(0, *[None,None,5,6,7])

        record = self.query.select(0,0,[1,1,1,1,1])[0]

        self.assertListEqual([0,1,5,6,7], record.columns)
    
    def test_select_non_existent(self):
        record = self.query.select(0,0,[1,1,1,1,1])
        
        self.assertFalse(record)

    def test_select_version_any_number_updates(self):
        # test if select version is running properly
        test_values = [0,1,2,3,4]
        self.query.insert(*test_values)
        test_dict = {}
        num_trials = 514
        
        for i in range(1,1+num_trials):
            change_index = i % 5
            test_values[change_index] = i
            test_dict[i] = test_values.copy()
            self.query.update(0, *test_values)
            
        for key in test_dict:
            version = key - num_trials
            record = self.query.select_version(0,0, [1]*5, version)[0]
            self.assertListEqual(test_dict[key], record.columns)

    def test_select_version_too_far_back(self):
        # testing if select version were to be given a version that does not exist, will it return base version
        # if there is only 2 versions but asked for 3 versions back, return base
        test_values = [0,1,2,3,4]
        self.query.insert(*test_values)
        
        self.query.update(0, *[None,None,5,6,7])

        record = self.query.select_version(0, 0, [1,1,1,1,1], -3)[0]

        self.assertListEqual(test_values, record.columns)

    def test_update_record_doesnt_exist(self):
        truth = self.query.update(0, [1,2,3,4,5])
        
        self.assertFalse(truth)

    def test_single_delete(self):
        test_values = [0,1,2,3,4]
        self.query.insert(*test_values)
        
        self.query.delete(0)
        record = self.query.select(0, 0, [1,1,1,1,1])
        test = record[0]
        print(test.columns)
        self.assertFalse(record)

if __name__ == '__main__':
    unittest.main()

