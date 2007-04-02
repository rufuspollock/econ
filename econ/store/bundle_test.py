import os
import unittest
import tempfile
import shutil

import econ.store
from bundle import DataBundle

def _makeTestData(basePath, title):
        metadata = 'title: %s' % title
        os.makedirs(basePath)
        ff = file(os.path.join(basePath, 'metadata.txt'), 'w')
        ff.write('[DEFAULT]\n')
        ff.write(metadata)
        ff.close()

class TestDataBundle:
    def setup_class(self):
        self.tmpDir = tempfile.mkdtemp()
        self.title = 'annakarenina'
        self.bundlePath = os.path.join(self.tmpDir, self.title)
    
    def teardown_class(self):
        shutil.rmtree(self.tmpDir)
    
    def test_writeBundle(self):
        self.startBundle = DataBundle()
        self.startBundle.id = self.title
        self.startBundle.metadata = { 'title' : self.title }
        self.startBundle.write(self.bundlePath)
    
    def test_readBundle(self):
        _makeTestData(self.bundlePath, self.title)
        bndl = DataBundle()
        bndl.read(self.bundlePath)
        assert (bndl.id == self.title)
        assert (bndl.metadata['title'] == self.title)


class TestMakeIndex:
    
    def setup_class(self):
        self.tmpDir = tempfile.mkdtemp()
        self.names = [ 'annakarenina', 'warandpeace' ]
        for name in self.names:
            _makeTestData(os.path.join(self.tmpDir, name), name)
        self.results = econ.store.make_index(self.tmpDir)
    
    def teardown_class(self):
        shutil.rmtree(self.tmpDir)
    
    def test_make_index1(self):
        assert (len(self.results) == len(self.names))
    
    def test_make_index2(self):
        for id, dataBundle in self.results.items():
            assert (id in self.names)

