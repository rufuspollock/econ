"""
Econ web interface via cherrypy.
"""
import cherrypy
import os

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
        storeIndex = [ (ii[0], get_title(ii[1].metadata)) for ii in index ]
        template.store_index = storeIndex
        return template.serialize()
        
    store.exposed = True

    def view(self, data_id=None, format='raw'):
        if data_id is None:
            return 'Please select a data set to view from the <a href="/store/">store</a>'
        import econ.store
        index = econ.store.index
        if data_id not in index.keys():
            return 'Error: There is no data set with that id'
        bundle = index[data_id]
        if format == 'raw':
            return '<pre>' + file(bundle.data_path).read() + '</pre>'
        elif format == 'html':
            import econ.www.templates.view_html
            template = econ.www.templates.view_html.Template()
            template.html_table = get_html_table(bundle)
            return template.serialize()
        else:
            return 'The format requested, [%s], is unsupported' % format
        
    view.exposed = True

def get_html_table(bundle):
    import econ.data.tabular
    reader = econ.data.tabular.ReaderCsv()
    writer = econ.data.tabular.WriterHtml({'id' : 'table_1'})
    ff = file(bundle.data_path)
    tabdata = reader.read(ff)
    html = writer.write(tabdata)
    return html
