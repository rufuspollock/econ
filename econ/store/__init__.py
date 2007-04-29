import os

import econ
import econ.store.bundle

def make_index(basePath):
    results = {}
    for root, dirs, files in os.walk(basePath):
        if 'metadata.txt' in files:
            bndl = econ.store.bundle.DataBundle()
            bndl.read(root)
            results[bndl.id] = bndl
    return results

def index():
    return make_index(econ.conf.get('DEFAULT', 'data_store_path'))
