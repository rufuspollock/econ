import os

import DataBundle
import econ

def make_index(basePath):
    results = {}
    for root, dirs, files in os.walk(basePath):
        if 'metadata.txt' in files:
            bundle = DataBundle.DataBundle()
            bundle.read(root)
            results[bundle.id] = bundle
    return results

index = make_index(econ.conf.get('DEFAULT', 'data_store_path'))
