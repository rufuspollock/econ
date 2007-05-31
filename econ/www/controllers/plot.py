import StringIO
import urllib
import genshi

from econ.www.lib.base import *

# Several steps:
# 1. generate plot
# 2. convert data to suitable format to use ...
#   csv
#   html 

class PlotController(BaseController):

    def help(self):
        return render_response('plot/help')

    def _get_data(self):
        limit = request.params.get('limit', '[:]')
        if request.params.has_key('data'):
            data = request.params.get('data')
        elif request.params.has_key('data_url'):
            data_url = request.params.get('data_url')
            if not data_url.endswith('.csv'):
                msg = 'At present only the viewing of csv format files is supported.'
                raise Exception(msg)
            data = urllib.urlopen(data_url).read()
        else:
            msg = 'No data source provided'
            raise Exception(msg)
        fileobj = StringIO.StringIO(data)
        fileobj = limit_fileobj(fileobj, limit)
        return fileobj
    
    def index(self):
        fileobj = None
        try:
            fileobj = self._get_data()
        except Exception, inst:
            msg = 'Error: %s' % inst
            c.error = msg
            return self.help()
        import genshi
        c.html_table = genshi.XML(get_html_table(fileobj))
        return render_response('plot/chart', strip_whitespace=False)
    
    def source(self):
        fileobj = None
        try:
            fileobj = self._get_data()
        except Exception, inst:
            msg = 'Error: %s' % inst
            c.error = msg
            return self.help()
        chart_code = self._get_chart_code(fileobj)
        return Response(chart_code, mimetype='text/plain')

    def _get_chart_code(self, fileobj):
        fileobj.seek(0)
        import econ.data.tabular
        reader = econ.data.tabular.ReaderCsv()
        tabdata = reader.read(fileobj)
        # rows to columns
        cols = econ.data.tabular.transpose(tabdata.data)
        c.datasets = []
        for ii in range(len(cols)):
            name = 'data%s' % ii
            c.datasets.append((name, str(cols[ii])))
        result = render('plot/chart_code')
        return result
         


    
    def test(self):
        c.html_table = '''<table>
    <tr>
        <td>0</td><td>1</td>
    </tr>
    <tr>
        <td>1</td><td>1</td>
    </tr>
    '''
        return render_response('plot/chart')


def get_html_table(fileobj):
    import econ.data.tabular
    reader = econ.data.tabular.ReaderCsv()
    writer = econ.data.tabular.WriterHtml({'id' : 'table_1'})
    tabdata = reader.read(fileobj)
    html = writer.write(tabdata)
    return html

def parse_limit(instr):
    # if a bad string just return None, None
    default = (None,None)
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
    
def limit_fileobj(fo, limit_str):
    start, end = parse_limit(limit_str)
    lines = fo.readlines()
    outlines = lines[start:end]
    outstr = ''.join(outlines)
    outfo = StringIO.StringIO(outstr)
    return outfo

