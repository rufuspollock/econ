"""
A DataBundle is a dataset along with its associated metadata

DataBundles are persisted and read from various backends:
  1. local file
  2. web
  3. database

At present only local file is supported.

Local File
**********

A DataBundle serialized to disk appears consists of:
  1. data file named data.<ext> where <ext> is the file type
    * (only ext=csv is presently supported)
  2. metadata file named metadata.txt
    * this file should conform to the python ConfigParser format (RFC 822) and 
    consist of a single section entitle [DEFAULT]
"""

import os
import shutil
import ConfigParser

class DataBundle(object):
    """A 'Data Bundle' that is dataset with associated metadata.
    """
    
    def __init__(self):
        self.id = ''
        self.metadata = {}
        self.path = None
        self.data_path = None
    
    def read(self, path):
        self.path = path
        # hack: assumes called data.csv
        # [[TODO: work this out in some proper way]]
        self.data_path = os.path.join(path, 'data.csv')
        self.id = os.path.basename(path)
        self.readMetadataFromFile(os.path.join(path, 'metadata.txt'))
    
    def readMetadataFromFile(self, path):
        cfp = ConfigParser.ConfigParser()
        cfp.read(path)
        self.metadata = cfp.defaults()
    
    def write(self, path):
        pass
    
    def __repr__(self):
        return 'DataBundle: ' + self.id + '\n' + str(self.metadata)

