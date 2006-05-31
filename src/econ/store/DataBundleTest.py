import os
import unittest
import tempfile
import shutil

import econ.store
from DataBundle import DataBundle

def _makeTestData(basePath, title):
        metadata = 'title: %s' % title
        os.makedirs(basePath)
        ff = file(os.path.join(basePath, 'metadata.txt'), 'w')
        ff.write('[DEFAULT]\n')
        ff.write(metadata)
        ff.close()

class DataBundleTest(unittest.TestCase):
    def setUp(self):
        self.tmpDir = tempfile.mkdtemp()
        self.title = 'annakarenina'
        self.bundlePath = os.path.join(self.tmpDir, self.title)
    
    def tearDown(self):
        shutil.rmtree(self.tmpDir)
    
    def test_writeBundle(self):
        self.startBundle = DataBundle()
        self.startBundle.id = self.title
        self.startBundle.metadata = { 'title' : self.title }
        self.startBundle.write(self.bundlePath)
    
    def test_readBundle(self):
        _makeTestData(self.bundlePath, self.title)
        bundle = DataBundle()
        bundle.read(self.bundlePath)
        self.failUnless(bundle.id == self.title)
        self.failUnless(bundle.metadata['title'] == self.title)


class MakeIndexTest(unittest.TestCase):
    
    def setUp(self):
        self.tmpDir = tempfile.mkdtemp()
        self.names = [ 'annakarenina', 'warandpeace' ]
        for name in self.names:
            _makeTestData(os.path.join(self.tmpDir, name), name)
        self.results = econ.store.make_index(self.tmpDir)
    
    def tearDown(self):
        shutil.rmtree(self.tmpDir)
    
    def test_make_index1(self):
        self.failUnless(len(self.results) == len(self.names))
    
    def test_make_index2(self):
        for id, dataBundle in self.results.items():
            self.failUnless(id in self.names)

if __name__ == '__main__':
    unittest.main() 

