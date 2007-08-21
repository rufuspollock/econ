# Miscellaneous helper utilities related to plotting

class Series:
    def __init__(self, xvalues, yvalues, label = ''):
        self.x = xvalues
        self.y = yvalues
        self.label = label
        # kept for backwards compatibility
        # TODO: remove (post 0.5 release?)
        self.xvalues = xvalues
        self.yvalues = yvalues


def seriesMaker(xvalues, function, label = ''):
    yvalues = []
    for xval in xvalues:
        yvalues.append(function(xval))
    return Series(xvalues, yvalues, label)


def parse_column(in_list, type_hint=None):
    """
    Assume either entry is numeric so either int or float.

    @return: tuple (parsed, skipped, problems) where skipped is list of indices
        that were skipped, problems is list of indices at which problem values
        were found and parsed is the new 'parsed' column.
    """
    # characters used to indicate no value
    skip_characters = [ '-', '', ' ' ]
    skipped = []
    problems = []
    out = []
    count = -1
    for xx in in_list:
        count += 1
        if xx in skip_characters:
            skipped.append(count)
            continue
        try:
            val = int(xx)
        except:
            try:
                val = float(xx)
            except:
                # first entry is probably a header
                if count != 0:
                    problems.append(count)
                continue
        out.append(val)
    return (out, skipped, problems)

def column(table):
    # get the columns
    # do type conversion
    pass
    
# -------------------
# matplotlib specific

def plotAssistant(listOfSeries, caption = '', xtitle = '', ytitle = ''):
    # matplotlib
    from pylab import *

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

## -------------------
## ploticus specific
## Note some of this code is a modified version of material originally found at:
## http://www.pyflag.net/pyflag/src/pyflag/Graph.py (which is GPL'd)

class Ploticus(object):
    '''Ploticus based plotting.

    @cvar out_format: The output format to use (svg/png/x11)
    '''
    out_format = 'png'
    ploticus = 'pl'

    def line(self, x, y):
        '''Plot a line chart.

        @arg x: x values
        @ arg y: y values
        '''
        # in_file_path, out_file_path, **kwargs):
        # self.cmd = '-prefab lines data=%(input)s x=1 y=14 y2=7 y3=8 y4=18 delim=comma header=yes' 
        self.cmd = ' -prefab lines x=1 y=2 delim=csv '
        self.input = self._make_csv(x,y)
        return self._run()

    def pie(self, values, lables, **kwargs):
        '''Plot a pie chart.

        @arg lables: A list of labels
        @arg values: A list of y values to use
        @arg opts: Options
        '''
        #Array with all the colors in it:
        colors = 'red orange green purple yellow blue magenta tan1 coral tan2 claret pink brightgreen brightblue limegreen yellowgreen lavender powderblue redorange lightorange'.split(' ')

        cmd = ' -prefab pie data=stdin labels=1 values=2 colorfld=3 delim=csv '
        options = [ '%s=%s' % (k,v) for k,v in kwargs.items() ]
        self.cmd = cmd + ' '.join(options)
        self.input = ''
        while len(colors) < len(values):
            colors += colors
        for i,j,k in zip(lables,values,colors):
            self.input += '%s,%s,%s\n' % (i,j,k)
        return self._run()

    def vbar(self, x, y, **kwargs):
        '''Plot a (vertical) bar chart.

        @arg x: A list of x values to use (can be names)
        @arg y: A list of y values to use (must be numeric)
        '''
        cmd = ' -prefab vbars x=1 y=2 delim=csv '
        options = [ '%s=%r' % (k,v) for k,v in kwargs.items() ]
        self.cmd = cmd + ' '.join(options)
        self.input = self._make_csv(x,y)
        return self._run()

    def _make_csv(self, xvals, yvals):
        out = ''
        for x,y in zip(xvals, yvals):
            out += '%s, %s\n' % (x,y)
        return out

    def _run(self):
        import popen2
        fullcmd = '%s -%s -data=stdin -o stdout %s ' % (self.ploticus, self.out_format,
            self.cmd)
        cstdout, cstdin, cstderr = popen2.popen3(fullcmd)
        cstdin.write(self.input)
        cstdin.close()
        data = cstdout.read()
        return data

