"""
Econ web interface via cherrypy.
"""
import os
import urllib
import StringIO

import paste.request

import kid
kid.enable_import(ext=['.html', '.kid'])

class EconWebInterface:

    def response(self, result):
        status = '200 OK'
        headers = [('Content-type','text/html')]
        self.start_response(status, headers)
        return [result]

    def __call__(self, environ, start_response):
        self.path = environ['PATH_INFO']
        self.start_response = start_response
        self.queryinfo = paste.request.parse_formvars(environ)
        if self.path == '/':
            return self.index()
        elif self.path.startswith('/current_value'):
            year = int(self.queryinfo.get('year', 2001))
            return self.current_value(year)
        elif self.path.startswith('/store'):
            return self.store()
        elif self.path.startswith('/view'):
            data_url = self.queryinfo.get('data_url', None)
            format = self.queryinfo.get('format', 'raw')
            return self.view(data_url, format)
        else:
            return self.response('Error')

    def index(self):
        import econ.www.templates.index
        template = econ.www.templates.index.Template()
        return self.response(template.serialize())

    def current_value(self, year=2001):
        try:
            import econ.www.templates.current_value
            template = econ.www.templates.current_value.Template()
            template.year = year
            template.ownPath = '/current_value/'
            currentValue = '100 (WARN: this utility is broken)'
            template.value = currentValue
            return self.response(template.serialize())
        except Exception, inst:
            return self.response('<p><strong>There was an error: ' +  str(inst) + '</strong></p>')

    def store(self):
        import econ.www.templates.store_index
        template = econ.www.templates.store_index.Template()
        import econ.store
        index = econ.store.index.items()
        def get_title(_dict):
            if _dict.has_key('title'):
                return _dict['title']
            else: return 'No title available'
        storeIndex = [ (ii[0], ii[1].metadata.get('title', 'No title available'), ii[1].data_path)
            for ii in index ]
        template.store_index = storeIndex
        return self.response(template.serialize())
        
    def view(self, data_url=None, format='raw'):
        if not data_url.endswith('.csv'):
            self.response('At present only the viewing of csv format files is
                    supported.')
        fileobj = None
        try:
            # have to wrap in a StringIO object urllib.fd does not support seek
            fileobj = StringIO.StringIO(urllib.urlopen(data_url).read())
        except Exception, inst:
            msg = 'Error: Unable to open the data file at %s because %s' % (data_url, inst)
            return self.response(msg)
        result = None
        if format == 'raw':
            result = '<pre>' + fileobj.read() + '</pre>'
        elif format == 'html':
            import econ.www.templates.view_html
            template = econ.www.templates.view_html.Template()
            template.html_table = get_html_table(fileobj)
            result = template.serialize()
        else:
            result = 'The format requested, [%s], is unsupported' % format
        return self.response(result)
        

def get_html_table(fileobj):
    import econ.data.tabular
    reader = econ.data.tabular.ReaderCsv()
    writer = econ.data.tabular.WriterHtml({'id' : 'table_1'})
    tabdata = reader.read(fileobj)
    html = writer.write(tabdata)
    return html
