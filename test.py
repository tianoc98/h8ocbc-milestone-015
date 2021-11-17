import unittest

from people import read_all
from movies import get_popularity
from config import app

class TestDirectors(unittest.TestCase):

    def test_read_all(self):
        self.assertIs(type(read_all()), list)
    

class TestMovies(unittest.TestCase):
    
    def test_getpopularity(self):
        self.assertIs(type(get_popularity()),list)

        
if __name__ == '__main__':
    unittest.main()