# Do not modify this file for personal use
# Instead make a copy to keep in your local checkout
import os
import sys
import re
import unittest

# Hack to get path to this directory
basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
srcpath = os.path.abspath(os.path.join(basepath, '../src/'))
sys.path.insert(0, basepath)
sys.path.insert(0, srcpath)

def makeTestSuite(testCaseRegex = ""):
    """
    Walk all directories in package searching for tests.
    Tests are identified by name which must be of form:
        <something>test.py (ignoring case)
    @param testCaseRegex: regex to select names of test cases. Optional
        parameter, defaulting to empty string.
    """
    allFiles = []
    for root, dirs, files in os.walk(srcpath):
        # get the path offset from srcpath
        # could use os.path.commonprefix
        pathOffset = root[len(srcpath) + 1:]
        test = re.compile(testCaseRegex + '.*test\.py$', re.IGNORECASE)
        files = filter(test.search, files)
        files = [pathOffset + '/' +  ff for ff in files]
        allFiles += files
    filenameToModuleName = lambda f: os.path.splitext(f)[0].replace('/','.')
    moduleNames = map(filenameToModuleName, allFiles)
    modules =[__import__(tmp1,'','','*') for tmp1 in moduleNames]
    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(load, modules))

if __name__ == "__main__":
    def usage():
        print 'test [<test_case_regex>]:'
        print '\tRun tests. If regex supplied run only those tests which match'
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        testCaseRegex = ''
        if len(sys.argv) > 2:
            testCaseRegex = sys.argv[2]
        unittest.TextTestRunner(verbosity=1).run(makeTestSuite(testCaseRegex))
    else:
        usage()
