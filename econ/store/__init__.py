import os
import logging

logger = logging.getLogger('econ.store')

import datapkg.index
from datapkg.package import Package

import econ

def make_index(basePath):
    ourindex = datapkg.index.SimpleIndex()
    for root, dirs, files in os.walk(basePath):
        if 'setup.py' in files or 'metadata.txt' in files:
            try:
                pkg = Package.load(root)
                ourindex.register(pkg)
            except Exception, inst:
                logger.warn('Failed to load package at %s because: %s' % (root,
                    inst))
    return ourindex

def get_data_path(package):
    if 'data.csv' in package.manifest:
        return os.path.join(package.path, 'data.csv')
    elif 'data.js' in package.manifest:
        return os.path.join(package.path, 'data.js')
    else:
        return None

def index():
    store_path = econ.get_config()['data_store_path']
    return make_index(store_path)
