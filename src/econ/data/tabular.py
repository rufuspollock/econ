"""
Tools for dealing with tabular data
"""

class TabularData(object):
    """Holder for tabular data

    Assume data organized in rows
    No type conversion so all data will be strings
    Properties:
        data: data itself provided as array of arrays
        header: associated header columns (if they exist)
    TODO: handling of large datasets (iterators?)
    """

    def __init__(self, data=[], header=[]):
        self.data = data 
        self.header = header

import csv
class ReaderCsv(object):
    """Read data from a csv file into a TabularData structure
    """

    def read(self, fileobj):
        """Read in a csv file and return a TabularData object
        @param: fileobj: file like object
        """
        tabData = TabularData()
        sample = fileobj.read()
        sniffer = csv.Sniffer()
        hasHeader = sniffer.has_header(sample)
        fileobj.seek(0)
        reader = csv.reader(fileobj, skipinitialspace=True)
        if hasHeader:
            tabData.header = reader.next()
        for row in reader:
            tabData.data.append(row)
        return tabData
    
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
