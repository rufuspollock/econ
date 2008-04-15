import os
import urllib
import StringIO

from econ.www.lib.base import *

import econ
import econ.store

class StoreController(BaseController):

    def index(self):
        import econ.store
        index = econ.store.index()
        bundles = index.values()
        storeIndex = []
        for bundle in bundles:
            title = bundle.metadata.get('title', 'No title available')
            storeIndex.append((h.url_for(bundle.id), title))
        c.store_index = storeIndex
        def mycmp(x,y):
            return cmp(x[1], y[1])
        c.store_index.sort(mycmp)
        return render('store/index')

    def _get_bundle(self, id):
        if id is None:
            msg = 'Please provide a bundle id.'
            raise Exception(msg) 
        import econ.store
        index = econ.store.index()
        try:
            bundle = index[id] 
        except:
            msg = 'The store does not contain a data bundle with id: %s' % id
            raise Exception(msg) 
        return bundle

    def view(self, id):
        bundle = self._get_bundle(id)
        c.title = bundle.metadata.get('title', 'No Title Provided')
        c.metadata = bundle.metadata
        # limit to a maximum of first 100 rows
        data_limit = 100
        c.data_url = h.url_for(controller='store', action='data', id=id,
                qualified=True)
        c.plot_data_url = h.url_for(controller='plot', action='chart', id=None, data_url=c.data_url,
                limit='[:100]')
        return render('store/view')

    def data(self, id):
        bundle = self._get_bundle(id)
        try:
            fileobj = file(bundle.data_path)
            result = fileobj.read()
        except:
            result = 'It looks like there is no data file for this dataset'
        response.headers['Content-Type'] = 'text/plain'
        return result

    def create(self):
        pass
        
