import os
import urllib

search_string = 'wheat price data'
base_page = 'http://www.ers.usda.gov/Data/Wheat/'
data_index = 'http://www.ers.usda.gov/Data/Wheat/WheatYearbook.aspx'

recent_data_url = 'http://www.ers.usda.gov/data/wheat/yearbook/WheatYearbookTables-Recent.xls'
all_data_url = 'http://www.ers.usda.gov/data/wheat/yearbook/WheatYearbookTables-Full.xls'
all_fn = 'data_original.xls'

VERBOSE = True

def download():
    if VERBOSE:
        print 'Starting download.'
        print 'Please be patient: the file is large so this may take some time.'
    urllib.urlretrieve(all_data_url, all_fn)

def info():
    import econ.data.tools as tl
    print tl.xls_info(all_fn)
    print tl.xls_sheet_info(all_fn, 1)

def parse():
    raise NotImplementedError()

def main():
    if not os.path.exists(all_fn):
        download()

if __name__ == '__main__':
    # main()
    info()
    # parse()
