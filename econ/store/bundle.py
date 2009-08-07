import os
import shutil
import ConfigParser
import uuid

import datapkg.distribution
from datapkg.package import Package


class IniBasedDistribution(datapkg.distribution.DistributionBase):
    keymap = {
        'id': 'name',
        'creator': 'author',
        'description': 'notes',
        'comments': 'notes',
        'licence': 'license',
        'tags': 'keywords',
        }

    @classmethod
    def from_path(self, path):
        pkg = Package()
        pkg.installed_path = path 
        fp = os.path.join(path, 'metadata.txt')
        # Read metadata from config.ini style fileobj
        cfp = ConfigParser.SafeConfigParser()
        cfp.readfp(open(fp))
        filemeta = cfp.defaults()
        if not 'name' in filemeta and 'id' in filemeta:
            filemeta['name'] = filemeta['id']
        extras = {}
        newmeta = dict(filemeta)
        if not 'extras' in newmeta:
            newmeta['extras'] = {}
        for inkey,value in filemeta.items():
            if inkey in Package.metadata_keys:
                continue
            elif inkey in self.keymap:
                actualkey = self.keymap.get(inkey, inkey)
                if actualkey == 'notes':
                    # TODO: do we need to trim leading '\n' that may result?
                    newmeta[actualkey] = newmeta.get(actualkey, '') + '\n' + value
                elif not actualkey in newmeta:
                    newmeta[actualkey] = value
            else:
                newmeta['extras'][inkey] = value
        pkg.update_metadata(newmeta)
        # TODO: deprecate this in favour of the manifest
        # TODO: default to 'data.csv' if no sections ...
        pkg.data_path = os.path.join(pkg.installed_path, 'data.csv')
        pkg.data_files = {}
        for section in cfp.sections():
            pkg.data_files[section] = dict(cfp.items(section))
        return self(pkg)

    def write(self):
        destpath = self.package.installed_path
        if not os.path.exists(destpath):
            os.makedirs(destpath)
        meta_path = os.path.join(destpath, 'metadata.txt')
        cfp = ConfigParser.SafeConfigParser(self.package.metadata)
        fo = file(meta_path, 'w')
        cfp.write(fo)
        fo.close()
    
