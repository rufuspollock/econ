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

