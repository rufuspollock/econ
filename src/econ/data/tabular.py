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

