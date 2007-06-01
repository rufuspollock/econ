import os
import urllib
import StringIO

from econ.www.lib.base import *

import econ
cfg = econ.conf

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
        return render_response('store/index')

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
        c.data_url = h.url_for(controller='store', action='data', id=id,
                qualified=True)
        c.plot_data_url = h.url_for(controller='plot', data_url=c.data_url)
        return render_response('store/view')

    def data(self, id):
        bundle = self._get_bundle(id)
        fileobj = file(bundle.data_path)
        result = fileobj.read()
        return Response(result, mimetype='text/plain')

    def create(self):
        pass
        
