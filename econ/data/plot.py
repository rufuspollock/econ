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
    @cvar ploticus: name of ploticus binary to call.

    Most functions take an extra kwargs variable. Important possible parameters
    are:
        * header='yes' (data has a header)
        * title=... (title for plot)
        * More details on
          <http://ploticus.sourceforge.net/doc/prefab_stdparms.html>

    Demo usage:

    >>> from econ.data.plot import Ploticus
    >>> pl = Ploticus()
    >>> x = [1,2,3]
    >>> y = [4,5,6]
    >>> graph_data = pl.line(x,y, title='My Plot')
    >>> fo = file('mygraph.png', 'wb')
    >>> fo.write(graph_data)
    >>> fo.close()
    '''
    out_format = 'png'
    ploticus = 'pl'
    colors = 'red orange green purple yellow blue magenta tan1 coral tan2 claret pink brightgreen brightblue limegreen yellowgreen lavender powderblue redorange lightorange'.split(' ')
    '''Array with all the colors in it'''

    def __init__(self, verbose=False):
        '''
        @arg verbose: be verbose (e.g. print command string)
        '''
        self.verbose = verbose

    def line(self, x, y, **kwargs):
        '''Plot a line chart.

        @arg x: A list of x values.
        @arg y: a list of y values.
        @arg **kwargs: additional key/value options to be passed to ploticus.
        @return: graph image data (binary).
        '''
        # in_file_path, out_file_path, **kwargs):
        # self.cmd = '-prefab lines data=%(input)s x=1 y=14 y2=7 y3=8 y4=18 delim=comma header=yes' 
        self.kwargs = kwargs
        self.cmd = ' -prefab lines x=1 y=2 delim=csv '
        self.input = self._make_csv(x,y)
        return self._run()

    def pie(self, values, lables, **kwargs):
        '''Plot a pie chart.

        @arg values: A list of y values to use.
        @arg lables: A list of labels.
        @arg **kwargs: additional key/value options to be passed to ploticus.
        @return: graph image data (binary).
        '''
        self.kwargs = kwargs

        cmd = ' -prefab pie labels=1 values=2 colorfld=3 delim=csv '
        self.input = ''
        colors = self.colors
        while len() < len(values):
            colors += self.colors
        for i,j,k in zip(lables,values,colors):
            self.input += '%s,%s,%s\n' % (i,j,k)
        return self._run()

    def vbar(self, x, y, **kwargs):
        '''Plot a (vertical) bar chart.

        @arg x: A list of x values to use (can be names).
        @arg y: A list of y values to use (must be numeric).
        @arg **kwargs: additional key/value options to be passed to ploticus.
        @return: graph image data (binary).
        '''
        self.kwargs = kwargs
        self.cmd = ' -prefab vbars x=1 y=2 delim=csv '
        self.input = self._make_csv(x,y)
        return self._run()

    def _make_csv(self, xvals, yvals):
        out = ''
        for x,y in zip(xvals, yvals):
            out += '%s, %s\n' % (x,y)
        return out
    
    def _make_cmd(self):
        options = [ '%s=%s' % (k,v) for k,v in self.kwargs.items() ]
        self.cmd = self.cmd + ' '.join(options)
        fullcmd = '%s -%s -data=stdin -o stdout %s ' % (self.ploticus, self.out_format,
            self.cmd)
        return fullcmd

    def _run(self):
        import popen2
        fullcmd = self._make_cmd()
        if self.verbose:
            print fullcmd
        cstdout, cstdin, cstderr = popen2.popen3(fullcmd)
        cstdin.write(self.input)
        cstdin.close()
        data = cstdout.read()
        if self.verbose:
            print cstderr.read()
        return data


class Diagram(object):

    def arrow(self, start, end):
        '''Wrap matplotlib stuff to make things simpler.'''
        # cannot get arrow to use a headwidth ...
        # pylab.annotate('', start, end, headwidth=
        pass
