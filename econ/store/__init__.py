import os
import logging

logger = logging.getLogger('econ.store')

import datapkg.index
from datapkg.package import Package

import econ
from econ.store.bundle import IniBasedDistribution

def make_index(basePath):
    ourindex = datapkg.index.SimpleIndex()
    for root, dirs, files in os.walk(basePath):
        if 'metadata.txt' in files:
            Dist = IniBasedDistribution
            try:
                dist = Dist.from_path(root)
                pkg = dist.package
                ourindex.register(pkg)
            except:
                logger.warn('Failed to load package at %s' % root)
        if 'setup.py' in files:
            try:
                pkg = Package.from_path(root)
                ourindex.register(pkg)
            except:
                logger.warn('Failed to load package at %s' % root)
    return ourindex

def index():
    store_path = econ.get_config()['data_store_path']
    return make_index(store_path)
