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
import uuid

def create(base_path):
    bndl = DataBundle()
    path = os.path.join(base_path, bndl.id)
    bndl.path = path
    bndl.write()
    return bndl

class DataBundle(object):
    """A 'Data Bundle' that is dataset with associated metadata.
    """

    def _set_path(self, value):
        self._path = value
        if self._path:
            self._meta_path = os.path.join(self._path, 'metadata.txt')
            self.data_path = os.path.join(self._path, 'data.csv')
        else:
            self._meta_path = None
            self.data_path = None

    def _get_path(self):
        return self._path
    
    def _del_path(self):
        del self._path

    def _set_id(self, value):
        self.metadata['id'] = value

    def _get_id(self):
        return self.metadata['id']

    def _del_id(self):
        del self.metadata['id']

    path = property(_get_path, _set_path, _del_path)
    id = property(_get_id, _set_id, _del_id)

    def __init__(self, id=None, path=None):
        # must be set first
        self.metadata = {}
        if id is None or id == '':
            self.id = str(uuid.uuid4())
        self.path = path
        self.data_files = {}

    def read(self, path):
        self.path = path
        # TODO: remove using file names for ids
        # set id from file name as default but may be overridden in metadata
        self.id = os.path.basename(path)
        fp = os.path.join(path, 'metadata.txt')
        self.read_metadata(file(fp))
    
    def read_metadata(self, fileobj):
        '''Read metadata from config.ini style fileobj.'''
        cfp = ConfigParser.SafeConfigParser()
        cfp.readfp(fileobj)
        filemeta = cfp.defaults()
        self.metadata.update(filemeta)
        for section in cfp.sections():
            self.data_files[section] = dict(cfp.items(section))
    
    def write(self):
        if not os.path.exists(self._path):
            os.makedirs(self._path)
        cfp = ConfigParser.SafeConfigParser(self.metadata)
        fo = file(self._meta_path, 'w')
        cfp.write(fo)
        fo.close()
    
    def __str__(self):
        repr = 'DataBundle: ' + self.id + '\n'
        repr += 'Title: ' + self.metadata['title'] + '\n\n'
        for key, value in self.metadata.items():
            repr += str(key) + ': ' + str(value) + '\n'
        return repr

