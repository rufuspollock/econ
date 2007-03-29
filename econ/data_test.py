import unittest
import StringIO
from data import *

class TimeSeriesTest(unittest.TestCase):
    
    def setUp(self):
        self.data = [ (1989, 4.4), (1990, 5.2), (1991, 5.3)]
        self.ts1 = TimeSeries(self.data)
    
    def testGetValue(self):
        self.assertEquals(self.ts1.getValue(1991), 5.3)
    
    def testGetValueOutsideRange(self):
        self.assertRaises(ValueError, self.ts1.getValue, 1986)
    
    def testGetValueInterpolated(self):
        self.assertEquals(self.ts1.getValue(1990.5), 5.25)
    
    def testGetTimeSeriesFromCsv(self):
        csvData = """1850,10.9
1851,10.6
1852,10.6
1853,11.5"""
        csvDataFileObject = StringIO.StringIO(csvData)
        ts1 = getTimeSeriesFromCsv(csvDataFileObject)
        self.assertEquals(ts1.getValue(1850), 10.9)
        
