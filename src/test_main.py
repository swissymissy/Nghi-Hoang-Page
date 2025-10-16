import unittest
from generate_page import extract_title

class MainFunctions(unittest.TestCase):

    def test_extract_title(self):
        md = """
# Normal title"""

        self.assertEqual("Normal title", extract_title(md))
    
    def test_extract_title_v2(self):
        md = """
   # Not title
# This is correct title"""

        self.assertEqual("This is correct title" , extract_title(md))

    def test_extract_tile_v3(self):
        md = """
    # There is no title in this markdown
Not a title"""
        with self.assertRaises(Exception):
            extract_title(md)