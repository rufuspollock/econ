# matplotlib
from pylab import *

class Series:
    def __init__(self, xvalues, yvalues, label = ''):
        self.xvalues = xvalues
        self.yvalues = yvalues
        self.label = label

def seriesMaker(xvalues, function, label = ''):
    yvalues = []
    for xval in xvalues:
        yvalues.append(function(xval))
    return Series(xvalues, yvalues, label)
    
def plotAssistant(listOfSeries, caption = '', xtitle = '', ytitle = ''):
    markers = ['+', ',', 'x', 'o', '.', 's', 'v', 's', '>', '<', '^']
    # colors = ['y', 'm', 'c', 'r', 'g', 'b', 'w', 'k']
    
    plotArgs = []
    if len(listOfSeries) >= 7:
        raise Exception('Cannot handle more than seven series and ' + len(listOfSeries) + ' series were supplied')
    for ii in range(len(listOfSeries)):
        line, = plot(listOfSeries[ii].xvalues, listOfSeries[ii].yvalues)
        line.set_marker(markers[ii])
        line.set_label(listOfSeries[ii].label)
    title(caption)
    legend(loc = 'upper right')
    xlabel(xtitle)
    ylabel(ytitle)

# TODO: make a proper test set
if __name__ == '__main__':
    xvals = [1,2,3]
    yvals = [x**2 for x in xvals]
    series1 = Series(xvals, yvals)
    # plotAssistant([series1], '', '', '', legend = 'upper right')