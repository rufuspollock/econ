import os

import bundle
import econ

def make_index(basePath):
    results = {}
    for root, dirs, files in os.walk(basePath):
        if 'metadata.txt' in files:
            bndl = bundle.DataBundle()
            bndl.read(root)
            results[bndl.id] = bndl
    return results

index = make_index(econ.conf.get('DEFAULT', 'data_store_path'))
