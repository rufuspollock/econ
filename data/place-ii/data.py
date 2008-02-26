from StringIO import StringIO
import zipfile
import urllib

import econ.data.tools as tl

# approx 656k
url = 'http://sedac.ciesin.columbia.edu/place/downloads/data/PLACEII_data_CIESIN_may07.zip'
# cache = os.path.abspath('./cache')

def download():
    fn = tl.url_basename(url) 
    urllib.urlretrieve(url, fn)

def unzip(): 
    fn = tl.url_basename(url) 
    zipfo = zipfile.ZipFile(file(fn))
    for name in zipfo.namelist():
        file(name, 'w').write(zipfo.read(name))

fns = [ 'National_Aggregates_of_Geospatial_Data_Collection_ PLACE-II.html',
        'PLACEII_DATA_CIESIN_MAY07.xls',
        ]

def get_data():
    import econ.data.tabular
    xlsreader = econ.data.tabular.XlsReader()
    variable_keys = {}
    for sht in [ xlsreader.read(file(fns[1]), sheet_index=1),
            xlsreader.read(file(fns[1]), sheet_index=2) ]:
        for row in sht.data:
            variable_keys[row[0]] = row[1]
    datasheets = [ xlsreader.read(file(fns[1]), sheet_index=ii).data for ii in
            range(3,7) ]
    return (variable_keys, datasheets)

def test_get_data():
    vars, data = get_data()
    assert vars[u'ISO3V10'] == 'International Standards Organization unique three-letter country or area code.'
    area1990 = data[0]
    assert area1990[9][5] == 627063.6

if __name__ == '__main__':
    download()
    unzip()
    # get_data()

