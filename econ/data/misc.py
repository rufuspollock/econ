class DataSniffer:
    '''Guess data type of a set of data by heuristics.'''
    # TODO
    pass

def floatify(value):
    # often numbers have commas in them like 1,030
    if value is None or not value.strip() or value.strip() == '-':
        return None
    if isinstance(value, basestring):
        v = value.replace(',', '')
    try:
        newval = float(v)
        return newval
    except:
        pass
    # will return original value if fails
    return date_to_float(value)

def floatify_matrix(matrix):
    return [ [ floatify(col) for col in row ] for row in matrix ]


import urlparse
import urllib
import os

class Retriever(object):
    def __init__(self, cache=''):
        '''
        @param cache: path to cache (if any)
        '''
        self.cache = cache
        if cache and not os.path.exists(cache):
            os.makedirs(cache)

    def retrieve(self, url, force=False):
        dest = self.filepath(url)
        if not os.path.exists(dest) or force:
            urllib.urlretrieve(url, dest)
        return file(dest) 

    def filepath(self, url):
        name = self.basename(url)
        dest = os.path.join(self.cache, name)
        return dest

    @classmethod
    def basename(self, url):
        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        result = path.split('/')[-1]
        if query:
            result += '?' + query
        return result

    @classmethod
    def dl(self, url, dest=None):
        '''Download a file from a url.

        Will use wget if available ...
        '''
        if not dest:
            dest = self.basename(url)
        urllib.urlretrieve(url, dest)


import dateutil.parser
import datetime
def date_to_float(date):
    '''Convert a date to float.

    Accepts either a date object or a string parseable to a date object
    
    @return: converted value or original if conversion fails
    '''
    if isinstance(date, basestring):
        try: # simple year
            return float(date)
        except:
            pass
        try:
            val = dateutil.parser.parse(date, default=datetime.date(1,1,1))
        except:
            return date
    else:
        val = date

    if isinstance(val, datetime.date):
        fval = val.year + val.month / 12.0 + val.day / 365.0
        return round(fval, 3)
    else:
        return val

def make_series(matrix, xcol, ycols_indices):
    '''Take a matrix and return series (i.e. list of tuples) correspond to
    specified column indices.
    '''
    # transpose
    cols = zip(*matrix)
    cols = floatify_matrix(cols)
    def is_good(value):
        if value is None: return False
        tv = str(value)
        stopchars = [ '', '-' ]
        if tv in stopchars:
            return False
        return True
    def is_good_tuple(tuple):
        return is_good(tuple[0]) and is_good(tuple[1])
    
    xcoldata = cols[xcol]
    # ycols = [ cols[idx] for idx in ycols_indices ]
    ycols = [ cols[ii] for ii in ycols_indices ]
    series = [ filter(is_good_tuple, zip(xcoldata, col)) for col in ycols ]
    return series

