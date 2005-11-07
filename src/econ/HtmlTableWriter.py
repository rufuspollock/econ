# Copyright (c) 2005, Rufus Pollock. All Rights Reserved
# Licensed under the GNU Public License (GPL) v2.0
# See the LICENSE file in the root of the distribution for details

import re

class HtmlTableWriter:
    """
    Write python matrices to xhtml
    """
    
    def __init__(self):
        # Whether to pretty print (indent) output
        self.doPrettyPrint = False
        # css class for table. Set as empty string if none wanted
        self.tableClass = 'data'
        # number of decimal places to use when rounding numerical values when
        # textifying for table
        self.decimalPlaces = 2
    
    def writeTable(self, data, caption = '', columnHeadings = [],
        rowHeadings = []):
        """
        Write matrix of data to xhtml table.
        Allow for addition of row and column headings
        
        @return xhtml table containing data
        
        @param data: table of data that makes up table
        @param caption: the caption for the table (if empty no caption created)
        """
        haveRowHeadings = False
        if len(rowHeadings) > 0:
            haveRowHeadings = True
        
        htmlTable = '<table'
        if self.tableClass != '':
            htmlTable += ' class="' + self.tableClass + '"'
        htmlTable += '>'
        
        # deal with caption
        if caption != '':
            htmlTable += self._writeTag('caption', caption)
        
        # deal with col headings
        # if we there are rowHeadings have to add blank column at front
        if len(columnHeadings) > 0:
            if haveRowHeadings:
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
        
        if self.doPrettyPrint:
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
            roundedResult = str(round(tagValue, self.decimalPlaces))
            if len(str(tagValue)) < len(roundedResult):
                return str(tagValue)
            else:
                return roundedResult
        else:
            return str(tagValue)