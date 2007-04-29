import StringIO
import urllib
import genshi

from econ.www.lib.base import *

# Several steps:
# 1. generate graph
# 2. convert data to suitable format to use ...
#   csv
#   html 

class GraphController(BaseController):

    def _usage(self):
        usage = '''To use this service:
Arguments:

    - limit: limit the section of the dataset we plot
            '''

    def index(self):
        data_url = request.params.get('data_url', '')
        limit = request.params.get('limit', '[:]')
        if not data_url.endswith('.csv'):
            return Response('At present only the viewing of csv format files is supported.')
        fileobj = None
        try:
            # have to wrap in a StringIO object urllib.fd does not support seek
            fileobj = StringIO.StringIO(urllib.urlopen(data_url).read())
            fileobj = limit_fileobj(fileobj, limit)
        except Exception, inst:
            msg = 'Error: Unable to open and process the data file at %s because %s' % (data_url, inst)
            return Response(msg)
        import genshi
        c.html_table = genshi.XML(get_html_table(fileobj))
        return render_response('graph/chart', strip_whitespace=False)
    
    def test(self):
        c.html_table = '''<table>
    <tr>
        <td>0</td><td>1</td>
    </tr>
    <tr>
        <td>1</td><td>1</td>
    </tr>
    '''
        return render_response('graph/chart')


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

