"""
Tools for dealing with tabular data
"""

class TabularData(object):
    """Holder for tabular data

    NB:
      * Assume data organized in rows.
      * No type conversion so all data will be as entered.

    Properties:
      * data: data itself provided as array of arrays
      * header: associated header columns (if they exist)

    TODO: handling of large datasets (iterators?)
    """

    def __init__(self, data=None, header=None):
        """
        Initialize object. If data or header not set they are defaulted to
        empty list.
        
        NB: must use None as default value for arguments rather than []
        because [] is mutable and using it will result in subtle bugs. See:
        'Default parameter values are evaluated when the function definition
        is executed.' [http://www.python.org/doc/current/ref/function.html]
        """
        self.data = []
        self.header = []
        if data is not None:
            self.data = data
        if header is not None:
            self.header = header

def transpose(data):
    # transpose a list of lists
    out = []
    numrows = len(data)
    if numrows == 0:
        return out
    numcols = len(data[0])
    if numcols == 0:
        return out
    for jj in range(numcols):
        newrow = []
        for ii in range(numrows):
            newrow.append(data[ii][jj])
        out.append(newrow)
    return out


import csv
import codecs
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8

    From: <http://docs.python.org/lib/csv-examples.html>
    """
    def __init__(self, f, encoding=None):
        if encoding:
            self.reader = codecs.getreader(encoding)(f)
        else: # already unicode so just return f
            self.reader = f

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode('utf-8')

class ReaderCsv(object):
    """Read data from a csv file into a TabularData structure

    Note that the csv module does *not* support unicode:
    
    > This version of the csv module doesn't support Unicode input. Also, there
    > are currently some issues regarding ASCII NUL characters. Accordingly,
    > all input should be UTF-8 or printable ASCII to be safe; see the examples
    > in section 9.1.5. These restrictions will be removed in the future.
    > <http://docs.python.org/lib/module-csv.html>

    Thus L{read} method requires uses an encoding.
    """

    def read(self, fileobj, encoding='utf-8'):
        """Read in a csv file and return a TabularData object

        @param fileobj: file like object.
        @param encoding: the encoding of the file like object. NB: will check
        if fileobj already in unicode in which case this is ignored.
        @return tabular data object (all values encoded as utf-8).
        """
        tabData = TabularData()

        sample = fileobj.read()
        # first do a simple test -- maybe sample is already unicode
        if type(sample) == unicode:
            encoded_fo = UTF8Recoder(fileobj, None)
        else:
            sample = sample.decode(encoding)
            encoded_fo = UTF8Recoder(fileobj, encoding)
        sample = sample.encode('utf-8')
        sniffer = csv.Sniffer()
        hasHeader = sniffer.has_header(sample)

        fileobj.seek(0)
        reader = csv.reader(encoded_fo, skipinitialspace=True)
        if hasHeader:
            tabData.header = reader.next()
        for row in reader:
            tabData.data.append(row)
        return tabData


from HTMLParser import HTMLParser
class HtmlReader(HTMLParser):
    '''Read data from HTML table into L{TabularData}.

    # TODO: tbody, thead etc
    # TODO: nested tables

    # TODO: will barf on bad html so may need to run tidy first ...
    # tidy -w 0 -b -omit -asxml -ascii
    '''
    def read(self, fileobj):
        '''Read data from fileobj.

        @return: L{TabularData} object (all content in the data part, i.e. no
        header).
        '''
        self.reset()
        self.feed(fileobj.read())
        tab = TabularData()
        tab.data = self._rows
        return tab

    def reset(self):
        HTMLParser.reset(self)
        self._rows = []
        self._row = []
        self._text = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self._row = []
            print tag
        elif tag == 'td':
            self._text = ''
        elif tag == 'br':
            self._text += '\n'

    def handle_endtag(self, tag):
        if tag == 'tr':
            self._rows.append(self._row)
        if tag == 'td':
            self._row.append(self._text)

    def handle_data(self, data):
        self._text += data.strip()

    
import re
class WriterHtml:
    """
    Write tabular data to xhtml
    """
    
    def __init__(self, table_attributes = {'class': 'data'}, decimal_places=2, do_pretty_print=False):
        """
        @do_pretty_print: whether to pretty print (indent) output
        @attributes: dictionary of html attribute name/value pairs to be
        added to the table element
        @decimal_places: number of decimal places to use when rounding numerical 
                        values when textifying for table
        """
        self.do_pretty_print = do_pretty_print
        self.table_attributes = table_attributes
        self.decimal_places = decimal_places
    
    def write(self, tabulardata, caption = '', rowHeadings = []):
        """
        Write matrix of data to xhtml table.
        Allow for addition of row and column headings
        
        @return xhtml table containing data
        
        @param data: table of data that makes up table
        @param caption: the caption for the table (if empty no caption created)
        """
        columnHeadings = tabulardata.header
        data = tabulardata.data
        haveRowHeadings = (len(rowHeadings) > 0)
        
        htmlTable = '<table'
        for key, value in self.table_attributes.items():
            htmlTable += ' %s="%s"' % (key, value)
        htmlTable += '>'
        
        # deal with caption
        if caption != '':
            htmlTable += self._writeTag('caption', caption)
        
        # deal with col headings
        # if we there are rowHeadings may want to add blank column at front
        numColHeads = len(columnHeadings)
        if numColHeads > 0:
            if haveRowHeadings and numColHeads == len(data[0]):
                # [[TODO: is this dangerous? should i make a copy ...]]
                columnHeadings.insert(0, '')
            htmlTable += self.writeHeading(columnHeadings)
        
        htmlTable += '<tbody>'
        
        for ii in range(0, len(data)):
            # have to add 1 as first row is headings
            if haveRowHeadings:
                htmlTable += self.writeRow(data[ii], rowHeadings[ii])
            else:
                htmlTable += self.writeRow(data[ii])
        
        htmlTable += '</tbody></table>'
        
        if self.do_pretty_print:
            return self.prettyPrint(htmlTable)
        else:
            return htmlTable
        
    def writeHeading(self, row):
        """
        Write heading for html table (<thead>)
        """
        result = '<thead><tr>'
        result += self.writeGeneralRow(row, 'th')
        result += '</tr></thead>'
        return result
    
    def writeRow(self, row, rowHeading = ''):
        result = ''
        if rowHeading != '':
            result = self._writeTag('th', rowHeading)
        result += self.writeGeneralRow(row, 'td')
        result = self._writeTag('tr', result)
        return result
    
    def writeGeneralRow(self, row, tagName):
        result = ''
        for ii in range(len(row)):
            result += self._writeTag(tagName, row[ii])
        return result
        
    def prettyPrint(self, html):
        """pretty print html using HTMLTidy"""
        # [[TODO: strip out html wrapper stuff that is added (head, body etc)
        import mx.Tidy
        return self.tabify(mx.Tidy.tidy(html, None, None, wrap = 0,
            indent = 'yes')[2])
        
    def tabify(self, instr, tabsize = 2):
        """
        tabify text by replacing spaces of size tabSize by tabs
        """
        whitespace = tabsize * ' '
        return re.sub(whitespace, '\t', instr)
        
    def _writeTag(self, tagName, value):
        return '<' + tagName + '>' + self._processTagValueToText(value) + \
            '</' + tagName + '>'
    
    def _processTagValueToText(self, tagValue):
        # if not already text then round
        if type(tagValue) != type('text'):
            roundedResult = str(round(tagValue, self.decimal_places))
            if len(str(tagValue)) < len(roundedResult):
                return str(tagValue)
            else:
                return roundedResult
        else:
            return str(tagValue)
