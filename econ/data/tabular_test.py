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

class WriterHtmlTest(unittest.TestCase):

    def setUp(self):
        rawData = [[1,1], [0,1]]
        self.indata1 = tabular.TabularData(data=rawData)
        self.writer1 = tabular.WriterHtml({'id':1, 'class': 'data'})

    def testSimple(self):
        indata1 = [[1,1], [0,1]]
        expected = '<table id="1" class="data"><tbody><tr><td>1</td><td>1</td></tr>'+\
            '<tr><td>0</td><td>1</td></tr></tbody></table>'
        out1 = self.writer1.write(self.indata1)
        self.assertEquals(expected, out1)
    
    def testColHeadings(self):
        self.indata1.header = ['x','y']
        caption = ''
        expected = '<table id="1" class="data"><thead><tr><th>x</th><th>y</th></tr>'+\
            '</thead><tbody><tr><td>1</td><td>1</td></tr><tr><td>0</td>' + \
            '<td>1</td></tr></tbody></table>'
        # no caption but headings
        out1 = self.writer1.write(self.indata1, caption)
        self.assertEquals(expected, out1)
    
    def testRowHeadings(self):
        self.indata1.header = ['x','y']
        rowHeadings = ['Date 1', 'Date 2']
        caption = ''
        expected = '<table id="1" class="data"><thead><tr><th></th><th>x</th>' + \
            '<th>y</th></tr></thead><tbody><tr><th>Date 1</th><td>1</td>' + \
            '<td>1</td></tr><tr><th>Date 2</th><td>0</td><td>1</td></tr>' + \
            '</tbody></table>'
        # no caption but headings
        out1 = self.writer1.write(self.indata1, caption, rowHeadings)
        self.assertEquals(expected, out1)
    
#    def testPrettyPrint(self):
#        in1 = '<table><tr><th>x</th><th>y</th></tr>' + \
#            '<tr><td>0</td><td>1</td></tr></table>'
#        print self.writer1.prettyPrint(in1)
