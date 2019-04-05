import unittest
import numpy as np
from pool import ProcessPool


class TestStringMethods(unittest.TestCase):

    def test_min_workers(self):
        big_data = [np.random.random((50, 50, 50)).tostring() for i in range(14)]
        pool = ProcessPool(min_workers=5, max_workers=10, mem_usage='0.1b')
        self.failureException


if __name__ == '__main__':
    unittest.main()