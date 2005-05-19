import os
import sys
import re
import unittest
import logging
import logging.config
logging.config.fileConfig('logging_basic.conf')

# Hack to get path to this directory
path = os.path.abspath(os.path.dirname(sys.argv[0]))
srcpath = os.path.abspath(os.path.join(path, '../src/'))
sys.path.append(path)
sys.path.append(srcpath)

def makeTestSuite():
	"""
	Walk all directories in econ package searching for tests.
	Tests are identified by name which must be of form: <something>test.py (ignoring case)
	"""
	allFiles = []
	for root, dirs, files in os.walk(srcpath):
		# get the path offset from srcpath
		# could use os.path.commonprefix
		pathOffset = root[len(srcpath) + 1:]
		test = re.compile("test\.py$", re.IGNORECASE)
		files = filter(test.search, files)
		files = [pathOffset + '/' +  ff for ff in files]
		allFiles += files
	filenameToModuleName = lambda f: os.path.splitext(f)[0].replace('/','.')
	moduleNames = map(filenameToModuleName, allFiles)
	modules =[__import__(tmp1,'','','*') for tmp1 in moduleNames]
	load = unittest.defaultTestLoader.loadTestsFromModule
	return unittest.TestSuite(map(load, modules))

if __name__ == "__main__":                   
	if len(sys.argv) > 1:
		if sys.argv[1] == 'test':
			unittest.TextTestRunner(verbosity=1).run(makeTestSuite())
		else:
			print 'ERROR: unknown argument'
	else:
		print 'ERROR: no argument supplied'
