import unittest
from StringIO import StringIO

import tabular

class TabularDataTest(unittest.TestCase):

    tabular = tabular.TabularData()

    def test_1(self):
        pass

class ReaderCsvTest(unittest.TestCase):
    
    csvdata = \
'''"header1", "header 2"
1, 2'''
    header = [ 'header1', 'header 2' ]
    data = [ ['1', '2'] ]
  
    def setUp(self):
        reader = tabular.ReaderCsv()
        fileobj = StringIO(self.csvdata)
        self.tab = reader.read(fileobj)

    def test_header(self):
        self.assertEqual(self.header, self.tab.header)

    def test_data(self):
        self.assertEqual(self.data, self.tab.data)

