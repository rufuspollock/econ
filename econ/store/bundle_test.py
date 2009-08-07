import os
import tempfile
import shutil
from StringIO import StringIO

import econ.store
from econ.store import IniBasedDistribution, Package

def _makeTestData(basePath, title):
    full_meta = \
'''[DEFAULT]
id : %s
title: %s
creator: abc
description: a long description
comments: here are some additional comments
requires-compilation: y

[data.csv]
title: ...

[xyz.png]
title: my graph
'''
    os.makedirs(basePath)
    ff = file(os.path.join(basePath, 'metadata.txt'), 'w')
    metadata = full_meta % (title, title)
    ff.write(metadata)
    ff.close()

class TestIniBasedDistribution:
    @classmethod
    def setup_class(self):
        self.tmpDir = tempfile.mkdtemp()
        self.title = 'annakarenina'
        self.dist_path = os.path.join(self.tmpDir, self.title)
    
    @classmethod
    def teardown_class(self):
        shutil.rmtree(self.tmpDir)

    def test_from_path(self):
        _makeTestData(self.dist_path, self.title)
        dist = IniBasedDistribution.from_path(self.dist_path)
        pkg = dist.package
        assert pkg.name == self.title, pkg
        assert pkg.title == self.title
        assert u'a long description' in pkg.notes
        assert u'additional comment' in pkg.notes
        assert pkg.author == u'abc'
        assert pkg.extras['requires-compilation'] == 'y'
        assert len(pkg.data_files) == 2
        assert pkg.data_files['data.csv']['title'] == '...'
    
    def test_write(self):
        name = 'abc'
        destpath = os.path.join(self.tmpDir, name)
        pkg = Package(name='abc', installed_path=destpath)
        dist = IniBasedDistribution(pkg)
        dist.write()
        metapath = os.path.join(destpath, 'metadata.txt')
        assert os.path.exists(destpath)
        assert os.path.exists(metapath)
        meta = file(metapath).read()
        assert '[DEFAULT]' in meta, meta
        assert 'name = abc' in meta, meta


class TestMakeIndex:
    @classmethod
    def setup_class(self):
        self.tmpDir = tempfile.mkdtemp()
        self.names = [ 'annakarenina', 'warandpeace' ]
        for name in self.names:
            _makeTestData(os.path.join(self.tmpDir, name), name)
        self.results = econ.store.make_index(self.tmpDir)
    
    @classmethod
    def teardown_class(self):
        shutil.rmtree(self.tmpDir)
    
    def test_make_index2(self):
        for pkg in self.results.list():
            assert (pkg.name in self.names)

