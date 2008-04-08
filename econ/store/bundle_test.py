import os
import tempfile
import shutil
from StringIO import StringIO

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

    def test___init__(self):
        bndl = DataBundle()
        id = bndl.id
        assert len(id) == 36
        assert bndl.path == None
    
    def test_read(self):
        _makeTestData(self.bundlePath, self.title)
        bndl = DataBundle()
        bndl.read(self.bundlePath)
        assert (bndl.id == self.title)
        assert (bndl.metadata['title'] == self.title)
    
    def test_write(self):
        bndl = DataBundle()
        destpath = os.path.join(self.tmpDir, bndl.id)
        bndl.path = destpath
        bndl.write()
        destpath = os.path.join(self.tmpDir, bndl.id)
        metapath = os.path.join(destpath, 'metadata.txt')
        assert os.path.exists(destpath)
        assert os.path.exists(metapath)
        meta = file(metapath).read()
        assert '[DEFAULT]\nid = ' in meta
    
    def test_create(self):
        bndl = econ.store.bundle.create(self.tmpDir)
        assert os.path.exists(bndl.path)
        assert len(bndl.id) == 36

    full_meta = \
'''[DEFAULT]
id : abc
title: mytitle

[data.csv]
title: ...

[xyz.png]
title: my graph
'''

    def test_read_metadata(self):
        bndl = econ.store.bundle.DataBundle()
        bndl.read_metadata(StringIO(self.full_meta))
        assert bndl.metadata['title'] == 'mytitle'
        assert len(bndl.data_files) == 2
        assert bndl.data_files['data.csv']['title'] == '...'
        

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

