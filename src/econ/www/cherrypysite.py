"""
Econ web interface via cherrypy.
"""
import os
import urllib
import StringIO

import cherrypy
import kid
kid.enable_import(suffixes=['.html', '.kid'])

class EconWebInterface:

    def index(self):
        out = '<h2><a href="current_value/">Current Value Calculator</a></h2>'
        out += '<h2><a href="store/">Data Store</a></h2>'
        return out
    index.exposed = True

    def current_value(self, year=2001):
        try:
            import econ.www.templates.current_value
            template = econ.www.templates.current_value.Template()
            template.year = year
            template.ownPath = '/current_value/'
            currentValue = '100 (WARN: this utility is broken)'
            template.value = currentValue
            return template.serialize()
        except Exception, inst:
            return '<p><strong>There was an error: ' +  str(inst) + '</strong></p>'
    current_value.exposed = True

    def store(self, data_id=None):
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
        return template.serialize()
        
    store.exposed = True

    def view(self, data_url=None, format='raw'):
        if not data_url.endswith('.csv'):
            return 'At present only the viewing of csv format files is supported.'
        fileobj = None
        try:
            # have to wrap in a StringIO object urllib.fd does not support seek
            fileobj = StringIO.StringIO(urllib.urlopen(data_url).read())
        except Exception, inst:
            msg = 'Error: Unable to open the data file at %s because %s' % (data_url, inst)
            return msg
        if format == 'raw':
            return '<pre>' + fileobj.read() + '</pre>'
        elif format == 'html':
            import econ.www.templates.view_html
            template = econ.www.templates.view_html.Template()
            template.html_table = get_html_table(fileobj)
            return template.serialize()
        else:
            return 'The format requested, [%s], is unsupported' % format
        
    view.exposed = True

def get_html_table(fileobj):
    import econ.data.tabular
    reader = econ.data.tabular.ReaderCsv()
    writer = econ.data.tabular.WriterHtml({'id' : 'table_1'})
    tabdata = reader.read(fileobj)
    html = writer.write(tabdata)
    return html
