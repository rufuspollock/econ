from StringIO import StringIO

import econ.data.tabular

class TestTabularData:

    tabular = econ.data.tabular.TabularData()

    def test_1(self):
        pass
    
class TestTranspose:

    def test_1(self):
        inlist = [
                [ 0, 1 ],
                [ 1, 0 ],
                ]
        exp = [
                [ 0, 1 ],
                [ 1, 0 ],
                ]
        out = econ.data.tabular.transpose(inlist)
        assert out == exp

class TestReaderCsv(object):
    
    csvdata = \
'''"header1", "header 2"
1, 2'''
    header = [ 'header1', 'header 2' ]
    data = [ ['1', '2'] ]
  
    def setup_method(self, name=''):
        reader = econ.data.tabular.ReaderCsv()
        fileobj = StringIO(self.csvdata)
        self.tab = reader.read(fileobj)

    def test_header(self):
        assert self.header == self.tab.header

    def test_data(self):
        assert self.data == self.tab.data


class TestReaderCsvUnicode(TestReaderCsv):
    csvdata = \
u'''"headi\xf1g", "header 2"
1, 2'''
    header = [ u'headi\xf1g'.encode('utf-8'), 'header 2' ]
    data = [ ['1', '2'] ]


class TestReaderCsvEncoded(TestReaderCsvUnicode):
    encoding = 'utf-16'
    csvdata = \
u'''"headi\xf1g", "header 2"
1, 2'''.encode(encoding)

    def setup_method(self, name=''):
        reader = econ.data.tabular.ReaderCsv()
        fileobj = StringIO(self.csvdata)
        self.tab = reader.read(fileobj, encoding=self.encoding)

class TestHtmlReader:

    inraw1 = '''
<table>
    <tr>
        <td>1</td><td>2</td>
    </tr>
    <tr>
        <td>3</td><td>4</td>
    </tr>
</table>
    '''
    in1 = StringIO(inraw1)
    
    exp1 = [ ['1', '2'],
            ['3', '4'],
            ]
    
    def test_1(self):
        reader = econ.data.tabular.HtmlReader()
        tab = reader.read(self.in1)
        assert tab.data == self.exp1


class TestWriterHtml:

    def setup_method(self, name=''):
        rawData = [[1,1], [0,1]]
        self.indata1 = econ.data.tabular.TabularData(data=rawData)
        self.writer1 = econ.data.tabular.WriterHtml({'id':1, 'class': 'data'})

    def testSimple(self):
        indata1 = [[1,1], [0,1]]
        expected = '<table id="1" class="data"><tbody><tr><td>1</td><td>1</td></tr>'+\
            '<tr><td>0</td><td>1</td></tr></tbody></table>'
        out1 = self.writer1.write(self.indata1)
        assert expected == out1
    
    def testColHeadings(self):
        self.indata1.header = ['x','y']
        caption = ''
        expected = '<table id="1" class="data"><thead><tr><th>x</th><th>y</th></tr>'+\
            '</thead><tbody><tr><td>1</td><td>1</td></tr><tr><td>0</td>' + \
            '<td>1</td></tr></tbody></table>'
        # no caption but headings
        out1 = self.writer1.write(self.indata1, caption)
        assert expected == out1
    
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
        assert expected == out1
    
#    def testPrettyPrint(self):
#        in1 = '<table><tr><th>x</th><th>y</th></tr>' + \
#            '<tr><td>0</td><td>1</td></tr></table>'
#        print self.writer1.prettyPrint(in1)
