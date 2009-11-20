import StringIO
import urllib2
import genshi
import datetime

import dateutil.parser
import simplejson

from econ.www.lib.base import *

import swiss.misc
import swiss.tabular

# Several steps:
# 1. generate plot
# 2. convert data to suitable format to use ...
#   csv
#   html 

class PlotController(BaseController):
    plotkit = False

    def index(self):
        return self.help()

    def help(self):
        return render('plot/help')

    def _get_data(self, dataset_id=None):
        limit = request.params.get('limit', '[:]')
        if dataset_id:
            offset = h.url_for(controller='store', action='data', id=dataset_id)
            data_url = '%s://%s%s' % (request.scheme, request.host, offset)
        elif request.params.has_key('data_url'):
            data_url = request.params.get('data_url')
        try:
            if request.params.has_key('data'):
                data = request.params.get('data')
                fileobj = StringIO.StringIO(data)
            elif data_url:
                # TODO: is this dangerous to allow any url to passed
                # what about ../../../ type urls?
                # if not data_url.endswith('.csv'):
                #    msg = 'At present only the viewing of csv format files is supported.'
                #    raise Exception(msg)
                # important to use fileobj to support large files
                fileobj = urllib2.urlopen(data_url)
            else:
                msg = 'No data source provided'
                raise Exception(msg)
            fileobj = limit_fileobj(fileobj, limit)
            self.tabular = self._tabular_data(fileobj)
        except Exception, inst:
            msg = 'Error: %s' % inst
            c.error = msg

    def _tabular_data(self, fileobj): 
        reader = swiss.tabular.ReaderCsv()
        tabdata = reader.read(fileobj)
        return tabdata

    def _set_format(self):
        format = request.params.get('format', 'html')
        if format == 'plain':
            response.headers['Content-Type'] = 'text/plain'

    def chart(self, id=None):
        self._get_data(id)
        if c.error:
            return self.help()
        c.html_table = genshi.XML(self.get_html_table(self.tabular))
        c.chart_code = genshi.HTML(self._get_chart_code(self.tabular))
        return render('plot/chart', strip_whitespace=False)

    def table(self, id=None):
        self._get_data(id)
        if not c.error:
            c.html_table = genshi.XML(self.get_html_table(self.tabular))
        self._set_format()
        return render('plot/table', strip_whitespace=False)
    
    def source(self, id=None):
        '''Get a chart in html/js source form.

        @arg format: if set to plain return result in text/plain.
        @arg xcol: the index of the data column to use for x values.
        '''
        self._get_data(id)
        if not c.error:
            chart_code = self._get_chart_code(self.tabular)
        else:
            chart_code = c.error
        self._set_format()
        return chart_code 

    def _get_chart_code(self, tabdata):
        xcol = request.params.get('xcol', 0)
        # create series for all columns (other than x)
        if not tabdata.data:
            return ''

        ycols = range(len(tabdata.data[0]))
        del ycols[xcol]
#         ycols = [ request.params.get('ycol0', 1) ]
#         for ii in range(1,4):
#             yvar_name = 'ycol%s' % ii
#             idx = request.params.get(yvar_name, None)
#             if idx:
#                 ycols.append(int(idx))
        cols = swiss.misc.make_series(tabdata.data, xcol, ycols)
        c.datasets = []
        for ii in range(len(cols)):
            if tabdata.header:
                name = tabdata.header[ycols[ii]]
                # escape entities that will give html problems
                name = name.replace('&', '+')
                name = name.replace('<', 'lt')
            else:
                name = 'data%s' % ii
            # use simplejson to ensure formatting is correct for js
            c.datasets.append(
                    (name, simplejson.dumps(cols[ii]))
                    )
        c.selected_series = []
        c.chart_type = request.params.get('chart_type', 'lines')
        result = render('plot/chart_code', fragment=True, format='xml')
        return result

    def get_html_table(self, tabdata):
        writer = swiss.tabular.WriterHtml({'id' : 'table_1'})
        html = writer.write_str(tabdata)
        return html

    def test(self):
        c.html_table = '''<table>
    <tr>
        <td>0</td><td>1</td>
    </tr>
    <tr>
        <td>1</td><td>1</td>
    </tr>
    '''
        return render('plot/chart')


def parse_limit(instr):
    # if a bad string just return None, None
    default = (0,None)
    if not (instr.startswith('[') and instr.endswith(']')):
        # log something?
        return default
    newstr = instr[1:-1]
    try:
        first, second = newstr.split(':')
    except:
        # log something?
        return default
    if first == '':
        first = None
    else:
        first = int(first)
    if second == '':
        second = None
    else:
        second = int(second)
    return (first, second)

# TODO: move this elsewhere (it should not be in the controller file ...
def limit_fileobj(fo, limit_str):
    # limit maximum files we will deal with to avoid barfing ...
    MAX_LINES = 10000
    start, end = parse_limit(limit_str)
    # be efficient
    # lines = fo.readlines()
    # outlines = lines[start:end]
    count = 0
    outlines = []
    for line in fo:
        if count >= start:
            outlines.append(line)
        if count == end:
            break
        if len(outlines) > MAX_LINES:
            msg = 'Requested %s lines of file but only allow max of %s' % \
                    ((start-end), MAX_LINES)
            raise Exception(msg) 
        count += 1
    outstr = ''.join(outlines)
    outfo = StringIO.StringIO(outstr)
    return outfo

