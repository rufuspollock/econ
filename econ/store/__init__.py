import os

import econ
import econ.store.bundle

def make_index(basePath):
    results = {}
    for root, dirs, files in os.walk(basePath):
        if 'metadata.txt' in files:
            bndl = econ.store.bundle.DataBundle()
            try:
                bndl.read(root)
                results[bndl.id] = bndl
            except:
                ## TODO: log error ...
                pass
    return results

def index():
    store_path = econ.get_config()['data_store_path']
    return make_index(store_path)
