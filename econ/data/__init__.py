from misc import *
from tabular import *

class TimeSeries(object):
    def __init__(self, dataPoints):
        """
        Datapoints should be of form (dateAsLong, value) e.g. (1991, xxx) or
        (1991.5, xxx).
        Assumes they are sorted and no duplicates
        [[TODO: support more input data types]]
        """
        self._dataPoints = dataPoints
        self._dates = []
        self._values = []
        for row in dataPoints:
            self._dates.append(float(row[0]))
            self._values.append(float(row[1]))
        import scipy.interpolate
        self.interpolator = scipy.interpolate.interp1d(self._dates, self._values)
    
    def getValue(self, date):
        if date < self._dates[0] or date > self._dates[-1]:
            raise ValueError('Date %s outside of range supported by this dataset' % date)
        else:
            if date in self._dates:
                return self._values[self._dates.index(date)]
            else:
                return self.interpolator(date)

def getTimeSeriesFromCsv(fileLikeObject):
    import csv
    reader = csv.reader(fileLikeObject)
    dataPoints = []
    for row in reader:
        dataPoints.append(row)
    return TimeSeries(dataPoints)
