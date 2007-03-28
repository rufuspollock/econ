"""
Econ web interface via cherrypy.
"""
import os
import urllib
import StringIO

import paste.request
import genshi
import genshi.template

import econ

cfg = econ.conf
template_path = cfg.get('web', 'template_dir')
template_loader = genshi.template.TemplateLoader([template_path],
        auto_reload=True)

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
        tmpl = template_loader.load('index.html')
        result = tmpl.generate().render()
        return self.response(result)

    def current_value(self, year=2001):
        try:
            currentValue = get_current_value(year)
            tmpl = template_loader.load('current_value.html')
            result = tmpl.generate(year=year,
                    ownPath='/current_value/',
                    value=currentValue)
            return self.response(result.render())
        except Exception, inst:
            return self.response('<p><strong>There was an error: ' +  str(inst) + '</strong></p>')

    def store(self):
        tmpl = template_loader.load('store_index.html')
        import econ.store
        index = econ.store.index.items()
        def get_title(_dict):
            if _dict.has_key('title'):
                return _dict['title']
            else: return 'No title available'
        storeIndex = [ (ii[0], ii[1].metadata.get('title', 'No title available'), ii[1].data_path)
            for ii in index ]
        result = tmpl.generate(store_index=storeIndex)
        return self.response(result.render())
        
    def view(self, data_url=None, format='raw'):
        if not data_url.endswith('.csv'):
            self.response('At present only the viewing of csv format files is supported.')
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
            tmpl = template_loader.load('view_html.html')
            html_table = get_html_table(fileobj)
            result = tmpl.generate(html_table=html_table)
            result = result.render()
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

def get_current_value(startYear, endYear=2002):
    import econ.data
    import econ.store
    import econ.DiscountRate
    databundle = econ.store.index['uk_price_index_1850-2002_annual']
    filePath = databundle.data_path
    ts1 = econ.data.getTimeSeriesFromCsv(file(filePath))
    discounter = econ.DiscountRate.DiscountRateHistorical(ts1)
    return discounter.getReturn(startYear, endYear)

